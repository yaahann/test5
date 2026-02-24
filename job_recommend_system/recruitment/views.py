from rest_framework import generics, permissions
from .models import Resume, Application
from .serializers import ResumeSerializer, ApplicationSerializer
from users.models import JobSeeker
from jobs.models import Job
from users.models import Recruiter
from rest_framework.response import Response

# 1. 简历管理视图 (上传 + 列表)
class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 只能看到自己的简历
        return Resume.objects.filter(seeker__user=self.request.user)

    def perform_create(self, serializer):
        # 上传时自动关联当前求职者
        seeker = JobSeeker.objects.get(user=self.request.user)
        serializer.save(seeker=seeker)

# 2. 投递管理视图 (投递 + 记录)
class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 只能看到自己的投递记录
        return Application.objects.filter(seeker__user=self.request.user).order_by('-apply_time')

    def perform_create(self, serializer):
        # 投递时自动关联当前求职者
        seeker = JobSeeker.objects.get(user=self.request.user)
        serializer.save(seeker=seeker)

# 3：简历删除/详情接口
class ResumeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(seeker__user=self.request.user)


# 新增：招聘者查看收到的投递记录
class RecruiterApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            recruiter = Recruiter.objects.get(user=user)
            # 逻辑：先找到该招聘者发布的所有职位，再找投递了这些职位的记录
            my_jobs = Job.objects.filter(recruiter=recruiter)
            return Application.objects.filter(job__in=my_jobs).order_by('-apply_time')
        except Recruiter.DoesNotExist:
            return Application.objects.none()

# 新增：招聘者修改投递状态 (比如改为面试/录用)
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 明确只允许 PATCH 方法
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # 安全检查：确保只有这个职位的发布者(招聘者)才能修改状态
        # 否则任何登录用户瞎猜一个ID都能改别人的简历状态
        if instance.job.recruiter.user != request.user:
            return Response({"detail": "您无权操作此投递记录"}, status=403)

        # 获取前端传来的 status
        new_status = request.data.get('status')
        if new_status is None:
            return Response({"detail": "缺少 status 字段"}, status=400)

        instance.status = new_status
        instance.save()
        return Response({"message": "状态更新成功", "status": instance.status})