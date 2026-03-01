from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. 自定义用户表 (对应文档中的 user 表)
class User(AbstractUser):
    # 角色类型选项
    ROLE_CHOICES = (
        (0, '管理员'),
        (1, '求职者'),
        (2, '招聘者'),
    )

    # 继承了 AbstractUser，已有 username, password, email, date_joined 等字段
    # [cite_start]下面添加文档中设计的额外字段 [cite: 108-114]

    phone = models.CharField(max_length=15, verbose_name='手机号', blank=True, null=True)
    role_type = models.SmallIntegerField(choices=ROLE_CHOICES, default=1, verbose_name='角色类型')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# [cite_start]2. 求职者信息表 (对应文档中的 job_seeker 表) [cite: 115-116]
class JobSeeker(models.Model):
    # 关联 User 表 (OneToOneField 确保一个用户只能有一个求职者档案)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile', verbose_name='关联用户')

    name = models.CharField(max_length=50, verbose_name='真实姓名', blank=True)
    gender = models.CharField(max_length=10, verbose_name='性别', choices=(('男', '男'), ('女', '女')), blank=True)
    birth_date = models.DateField(verbose_name='出生日期', blank=True, null=True)
    education = models.CharField(max_length=20, verbose_name='最高学历', blank=True)  # 如：本科
    major = models.CharField(max_length=50, verbose_name='专业', blank=True)

    # [cite_start]关键字段：技能标签，用于推荐算法 [cite: 116]
    exp_job = models.CharField(max_length=50, verbose_name='期望职位', blank=True, default='')
    skills = models.CharField(max_length=255, verbose_name='技能标签', blank=True,
                              help_text='多个标签用逗号分隔，如: Python,Vue')
    exp_city = models.CharField(max_length=50, verbose_name='期望工作城市',blank=True, default='')
    job_status = models.SmallIntegerField(default=0, verbose_name='求职状态', choices=((0, '待业'), (1, '在职')))
    experience = models.TextField(verbose_name='工作经历', blank=True)

    class Meta:
        verbose_name = '求职者资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name if self.name else self.user.username


# [cite_start]3. 招聘者/企业信息表 (对应文档中的 recruiter 表) [cite: 117-118]
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile',
                                verbose_name='关联用户')

    company_name = models.CharField(max_length=100, verbose_name='公司名称',blank=True)
    company_scale = models.CharField(max_length=50, verbose_name='公司规模', blank=True)
    industry = models.CharField(max_length=50, verbose_name='所属行业', blank=True)
    description = models.TextField(verbose_name='公司简介', null=True, blank=True)
    company_addr = models.CharField(max_length=255, verbose_name='企业地址', blank=True)

    # 营业执照等文件通常需要 FileField
    license = models.FileField(upload_to='licenses/%Y/%m/', verbose_name='认证文件', blank=True)

    # [cite_start]审核状态 [cite: 118]
    audit_status = models.SmallIntegerField(default=0, verbose_name='审核状态',
                                            choices=((0, '待审'), (1, '通过'), (2, '拒绝')))

    class Meta:
        verbose_name = '招聘者/企业资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company_name if self.company_name else f"{self.user.username} (待完善企业)"

# 4. Message 站内私信
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送方')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                 verbose_name='接收方')

    content = models.TextField(verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '站内私信'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']  # 最新消息排在最前面

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"