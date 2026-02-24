from rest_framework import serializers
from .models import Job
from rest_framework.validators import UniqueValidator



class JobSerializer(serializers.ModelSerializer):
    # 显示发布者的公司名称（只读），方便前端展示
    company_name = serializers.CharField(source='recruiter.company_name', read_only=True)
    # 自动关联当前登录的招聘者（用户必须是Recruiter类型）
    recruiter = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = '__all__'
        # 发布者ID和创建时间由后台自动处理，前端只读
        read_only_fields = ('recruiter', 'create_time', 'status')