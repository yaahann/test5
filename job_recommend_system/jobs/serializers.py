from rest_framework import serializers
from .models import Job,JobCollection
from rest_framework.validators import UniqueValidator



class JobSerializer(serializers.ModelSerializer):
    # 显示发布者的公司名称（只读），方便前端展示
    company_name = serializers.CharField(source='recruiter.company_name', read_only=True)
    # 显式地把关联的招聘者（公司）的 ID 传递给前端
    recruiter_id = serializers.IntegerField(source='recruiter.id', read_only=True)
    # 自动关联当前登录的招聘者（用户必须是Recruiter类型）
    recruiter = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = '__all__'
        # 发布者ID和创建时间由后台自动处理，前端只读
        read_only_fields = ('recruiter', 'create_time', 'status')

# 职位收藏序列化器
class JobCollectionSerializer(serializers.ModelSerializer):
    # 嵌套一个 JobSerializer，这样前端获取收藏列表时，能直接拿到公司的名称、薪资等职位详细信息
    job_info = JobSerializer(source='job', read_only=True)

    class Meta:
        model = JobCollection
        fields = ['id', 'job', 'job_info', 'collect_time']
        read_only_fields = ['seeker', 'collect_time']