from rest_framework import generics, permissions,status
from .models import Job,JobCollection,News
from .serializers import JobSerializer,JobCollectionSerializer,NewsSerializer
from users.models import Recruiter,JobSeeker
from rest_framework.views import APIView # 引入 APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 职位列表与发布视图
# jobs/views.py

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 配置搜索
    filter_backends = [filters.SearchFilter]
    search_fields = ['job_title', 'description', 'recruiter__company_name', 'city']

    def get_queryset(self):
        # 1. 基础查询：只显示招聘中(status=1)的，按时间倒序
        queryset = Job.objects.filter(status=1).order_by('-create_time')

        # 2. 如果前端传了 recruiter_id，就只看这个公司的
        recruiter_id = self.request.query_params.get('recruiter_id')
        if recruiter_id:
            queryset = queryset.filter(recruiter_id=recruiter_id)

        # 城市筛选 (模糊匹配)
        city = self.request.query_params.get('city')
        if city and city != '全部':
            queryset = queryset.filter(city__icontains=city)

        # 学历筛选 (精确匹配)
        education_req = self.request.query_params.get('education_req')
        if education_req and education_req != '不限':
            queryset = queryset.filter(education_req=education_req)

        # 经验筛选 (精确匹配)
        exp_req = self.request.query_params.get('exp_req')
        if exp_req and exp_req != '不限':
            queryset = queryset.filter(exp_req=exp_req)

        # 职位类型筛选 (精确匹配)
        job_type = self.request.query_params.get('job_type')
        if job_type and job_type != '全部':
            queryset = queryset.filter(job_type=job_type)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user.role_type != 2:
            raise permissions.exceptions.PermissionDenied("只有招聘者账号可以发布职位")

        try:
            # 尝试获取招聘者个人资料
            recruiter_profile = Recruiter.objects.get(user=user)
        except Recruiter.DoesNotExist:
            # 如果找不到，返回一个清晰的错误给前端，而不是直接 500
            from rest_framework.exceptions import ValidationError
            raise ValidationError("您的招聘者资料不完整，请先完善企业信息。")
        # 检查企业资质审核状态
        if recruiter_profile.audit_status != 1:  # 1 代表审核通过
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("您的企业资质尚未通过审核，暂时无法发布新职位。")

        serializer.save(recruiter=recruiter_profile, status=0)


# 2. 职位详情与操作视图 (查看/修改/删除)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 只有职位的发布者才能修改/删除
    def get_queryset(self):
        # 如果是修改/删除请求，只能操作自己的职位
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Job.objects.filter(recruiter__user=self.request.user)
        return Job.objects.all()

    # 但凡招聘者修改了职位信息，状态强制变为待审(0)
    def perform_update(self, serializer):
        serializer.save(status=0)

    # 重写 retrieve 方法，在获取详情时实时计算当前求职者的匹配度
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 判断：如果当前是登录状态，且是求职者 (role_type == 1)
        if request.user.is_authenticated and request.user.role_type == 1:
            try:
                seeker = JobSeeker.objects.get(user=request.user)
                # 提取求职者画像
                user_features = [(seeker.skills or "")*3, seeker.education or "", seeker.major or "",
                                 seeker.experience or "",(seeker.exp_job or "")*3,(seeker.exp_city or "")*3]
                user_text = " ".join(user_features)

                if user_text.strip():
                    # 提取当前这个岗位的画像
                    job_features = [
                        instance.job_title * 3, (instance.job_tags or "") * 3, instance.description or "",
                        instance.city * 3, instance.education_req, instance.exp_req
                    ]
                    job_text = " ".join(job_features)

                    # 分词与向量化
                    user_words = " ".join(jieba.lcut(user_text))
                    job_words = " ".join(jieba.lcut(job_text))

                    vectorizer = TfidfVectorizer()
                    tfidf_matrix = vectorizer.fit_transform([user_words, job_words])

                    # 计算两个文本的余弦相似度
                    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

                    # 存入返回的 JSON 数据中
                    if score > 0.05:
                        data['match_score'] = round(score * 100, 1)
                    else:
                        data['match_score'] = 0
            except Exception as e:
                # 容错处理，如果计算失败不影响详情页的正常展示
                pass

        return Response(data)


# 3：招聘者查看自己发布的职位列表
class RecruiterJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 找到当前用户的招聘者档案
        try:
            recruiter = Recruiter.objects.get(user=user)
            return Job.objects.filter(recruiter=recruiter).order_by('-create_time')
        except Recruiter.DoesNotExist:
            return Job.objects.none()


# 4.修改职位状态视图
class JobStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        # 1. 找到职位，并确保它是当前用户发布的
        job = get_object_or_404(Job, pk=pk)

        # 2. 权限校验
        if job.recruiter.user != request.user:
            return Response({"detail": "无权操作"}, status=403)

        # 3. 修改状态
        # 前端传 { status: 2 } (2代表停止招聘，1代表招聘中)
        new_status = request.data.get('status')
        if new_status == 1:
            return Response({"detail": "职位必须经过管理员审核通过后才能上架，请提交审核"}, status=400)
        if new_status is not None:
            job.status = new_status
            job.save()
            return Response({"message": "状态已更新"})

        return Response({"detail": "参数错误"}, status=400)


# 5.职位收藏视图
class JobCollectionView(generics.ListCreateAPIView):
    serializer_class = JobCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 获取当前求职者的收藏列表
        try:
            seeker = JobSeeker.objects.get(user=self.request.user)
            return JobCollection.objects.filter(seeker=seeker).order_by('-collect_time')
        except JobSeeker.DoesNotExist:
            return JobCollection.objects.none()

    def create(self, request, *args, **kwargs):
        # 验证是否为求职者
        try:
            seeker = JobSeeker.objects.get(user=request.user)
        except JobSeeker.DoesNotExist:
            return Response({"detail": "只有求职者可以收藏职位"}, status=status.HTTP_403_FORBIDDEN)

        job_id = request.data.get('job')
        if not job_id:
            return Response({"detail": "缺少 job 参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 校验职位是否存在
        try:
            Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"detail": "职位不存在"}, status=status.HTTP_404_NOT_FOUND)

        # get_or_create 逻辑：如果有记录则获取，没有则创建
        collection, created = JobCollection.objects.get_or_create(seeker=seeker, job_id=job_id)

        if not created:
            # 取消收藏
            collection.delete()
            return Response({"message": "已取消收藏", "is_collected": False}, status=status.HTTP_200_OK)
        else:
            # 收藏成功（补全这个分支的响应）
            return Response({"message": "收藏成功", "is_collected": True}, status=status.HTTP_201_CREATED)

# 6.获取待审核职位列表
class AdminPendingJobsView(generics.ListAPIView):
    queryset = Job.objects.filter(status=0).order_by('-create_time')
    serializer_class = JobSerializer
    # 同样使用上面自定义的 IsAdminUser (需要你把 IsAdminUser 类也复制到这个文件顶部)
    permission_classes = [permissions.IsAuthenticated]  # 为了简便，这里你也可以直接在 get_queryset 里判断 role_type

    def get_queryset(self):
        if self.request.user.role_type != 0:
            return Job.objects.none()
        return super().get_queryset()

# 7.职位审核操作
class AdminAuditJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role_type != 0:
            return Response({"detail": "无权操作"}, status=403)

        job = get_object_or_404(Job, pk=pk)
        new_status = request.data.get('status')
        if new_status in [1, 2]:  # 1通过(招聘中) 2拒绝(已下架)
            job.status = new_status
            job.save()
            return Response({"message": "职位审核完成"})
        return Response({"detail": "状态参数错误"}, status=400)

# 获取所有职位（无论状态）用于看板
class AdminAllJobsView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-create_time')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role_type != 0:
            return Job.objects.none()
        return super().get_queryset()

# 公开的资讯列表
class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-publish_time')
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny] # 允许任何人免登录查看
# 公开的单条资讯详情接口
class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny] # 允许免登录查看

    # 重写 get_object 方法，每次被请求时，阅读量自动 +1
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj