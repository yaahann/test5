from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, JobSeeker , Recruiter
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, JobSeekerSerializer,RecruiterSerializer
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


