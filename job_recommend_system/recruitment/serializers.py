from rest_framework import serializers
from .models import Resume, Application
from jobs.serializers import JobSerializer  # 用于在投递记录里展示职位详情

# 1. 简历序列化器
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('seeker', 'create_time')

# 2. 投递记录序列化器
class ApplicationSerializer(serializers.ModelSerializer):
    # 嵌套 JobSerializer，这样前端获取投递记录时，能直接看到是哪个职位的
    job_info = JobSerializer(source='job', read_only=True)
    # 2. 获取简历标题 (方便显示是谁的简历)
    resume_title = serializers.ReadOnlyField(source='resume.resume_title')
    # 3. 直接获取简历文件的 URL
    resume_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('seeker', 'status', 'apply_time', 'hr_feedback')

    # 验证逻辑：防止重复投递同一个职位
    def validate(self, data):
        user = self.context['request'].user
        job = data['job']
        # 查询该用户是否已经投递过该职位
        if Application.objects.filter(seeker__user=user, job=job).exists():
            raise serializers.ValidationError("您已经投递过该职位，请勿重复投递。")
        return data

    def get_resume_file_url(self, obj):
        try:
            # 获取文件的相对路径 (例如 /media/resumes/xxx.pdf)
            return obj.resume.resume_file.url
        except:
            return None