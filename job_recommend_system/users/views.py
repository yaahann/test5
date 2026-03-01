from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, JobSeeker , Recruiter,Message
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, JobSeekerSerializer,RecruiterSerializer,MessageSerializer
from jobs.models import Job
from recruitment.models import Application
# 1. 注册接口
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# 2. 自定义登录接口 (用于返回带用户名的Token)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 3. 求职者个人资料接口 (查看 + 修改)
class JobSeekerDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # 直接返回当前登录用户的 JobSeeker 对象
        # 如果没有(比如刚注册)，就自动创建一个空的
        obj, created = JobSeeker.objects.get_or_create(user=self.request.user)
        return obj


# 4.招聘者公司详情接口 （查看+修改）
class RecruiterDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # 返回当前登录用户的 Recruiter 对象
        # 如果没有，就自动创建一个空的 (由于你已经把 company_name 设为 blank=True，这里可以直接创建)
        obj, created = Recruiter.objects.get_or_create(user=self.request.user)
        return obj

    def perform_update(self, serializer):
        instance = serializer.save()
        # 如果企业原本是被拒绝状态(2)，重新修改保存资料后，自动变回待审(0)
        if instance.audit_status == 2:
            instance.audit_status = 0
            instance.save()

# 5.公开的公司列表 (用于"公司"板块)
class PublicCompanyListView(generics.ListAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer # 我们需要确保 serializers.py 里有这个
    permission_classes = [permissions.AllowAny] # 允许任何人访问


# 6.公开的公司详情 (用于"企业详情页")
class PublicCompanyDetailView(generics.RetrieveAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = [permissions.AllowAny] # 允许不登录访问

# 1. 定义一个通用的管理员权限校验类
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role_type == 0)

# 2. 获取待审核企业列表
class AdminPendingRecruitersView(generics.ListAPIView):
    queryset = Recruiter.objects.filter(audit_status=0).order_by('-id')
    serializer_class = RecruiterSerializer
    permission_classes = [IsAdminUser]

# 3. 企业审核操作 (通过/拒绝)
class AdminAuditRecruiterView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        recruiter = get_object_or_404(Recruiter, pk=pk)
        new_status = request.data.get('audit_status')
        if new_status in [1, 2]:  # 1通过 2拒绝
            recruiter.audit_status = new_status
            recruiter.save()
            return Response({"message": "企业审核完成"})
        return Response({"detail": "状态参数错误"}, status=400)

# 平台数据统计大盘接口
class AdminStatsView(APIView):
    # 复用之前写的 IsAdminUser 权限类
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1. 用户相关统计
        total_users = User.objects.count()
        total_seekers = JobSeeker.objects.count()
        total_recruiters = Recruiter.objects.count()

        # 2. 职位相关统计
        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(status=1).count()  # 招聘中的职位
        pending_jobs = Job.objects.filter(status=0).count()  # 待审核的职位

        # 3. 互动数据统计
        total_applications = Application.objects.count()  # 简历投递总次数

        return Response({
            "total_users": total_users,
            "total_seekers": total_seekers,
            "total_recruiters": total_recruiters,
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "pending_jobs": pending_jobs,
            "total_applications": total_applications
        })

# 获取所有求职者用于看板
class AdminAllSeekersView(generics.ListAPIView):
    queryset = JobSeeker.objects.all().order_by('-id')
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAdminUser]

# 获取所有企业（无论状态）用于看板
class AdminAllRecruitersView(generics.ListAPIView):
    queryset = Recruiter.objects.all().order_by('-id')
    serializer_class = RecruiterSerializer
    permission_classes = [IsAdminUser]


# 1. 发送消息接口
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        if not receiver_id or not content:
            return Response({"detail": "缺少接收人或消息内容"}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"detail": "接收方用户不存在"}, status=404)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )
        return Response({"message": "发送成功"}, status=201)


# 2. 获取我的消息列表接口
class MyMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)


# 3. 标记消息为已读接口
class MarkMessageReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            msg = Message.objects.get(pk=pk, receiver=request.user)
            msg.is_read = True
            msg.save()
            return Response({"message": "已读"})
        except Message.DoesNotExist:
            return Response({"detail": "消息不存在"}, status=404)
