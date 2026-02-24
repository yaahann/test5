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
        # 1. 正常创建 User 账号
        user = User(
            username=validated_data['username'],
            role_type=validated_data.get('role_type'),
            # 把其它需要的字段也填上，比如 phone, email 等
        )
        user.set_password(validated_data['password'])
        user.save()

        # 2. 根据前端传来的 role_type，自动创建关联的档案表
        # 注意：这里的 1 和 2 请替换成你 models.py 中实际定义的 role_type 值
        # 比如你的 role_type 是字符串 'recruiter' 还是数字 2
        role = validated_data.get('role_type')
        if role == 2:  # 假设 2 代表招聘者
            Recruiter.objects.create(user=user)
        else:          # 默认或者 1 代表求职者
            JobSeeker.objects.create(user=user)

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