from rest_framework import generics, permissions,status
from .models import Job,JobCollection
from .serializers import JobSerializer,JobCollectionSerializer
from users.models import Recruiter,JobSeeker
from rest_framework.views import APIView # 引入 APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters

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
        # 例如：/api/jobs/?recruiter_id=5
        recruiter_id = self.request.query_params.get('recruiter_id')
        if recruiter_id:
            queryset = queryset.filter(recruiter_id=recruiter_id)

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