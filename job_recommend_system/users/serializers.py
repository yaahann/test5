from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, JobSeeker,Recruiter

# 1. 注册序列化器 (已有的)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'role_type', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# 2. 自定义Token序列化器 (新增！解决 MyTokenObtainPairSerializer 报错)
# 作用：让登录返回的 Token 里包含用户名和角色信息，方便前端使用
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role_type'] = user.role_type
        return token

    # 作用：让登录接口的返回数据里直接包含 role_type，不用前端去解密 Token
    def validate(self, attrs):
        data = super().validate(attrs)
        # 将用户信息添加到返回的 JSON 数据中
        data['role_type'] = self.user.role_type
        data['username'] = self.user.username
        return data


# 3. 求职者资料序列化器 (新增！解决 JobSeekerSerializer 报错)
class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = '__all__'
        read_only_fields = ('user',)  # 用户关联字段只读，不让改

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__' # 或者只暴露 ['id', 'company_name', 'logo', 'description']