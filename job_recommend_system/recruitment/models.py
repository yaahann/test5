from django.db import models
from django.utils import timezone


# [cite_start]4. 简历表 (对应文档中的 resume 表) [cite: 119-124]
class Resume(models.Model):
    # 关联求职者
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='求职者')

    resume_title = models.CharField(max_length=50, verbose_name='简历标题')

    # 这里使用 FileField，Django 会自动处理文件上传到 MEDIA_ROOT 目录
    # 对应文档中的 resume_file_url，实际上存的是文件路径
    resume_file = models.FileField(upload_to='resumes/%Y/%m/', verbose_name='简历附件')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '简历附件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resume_title


# [cite_start]6. 投递记录表 (对应文档中的 application 表) [cite: 127-128]
class Application(models.Model):
    # 状态常量
    STATUS_CHOICES = (
        (0, '已投递'),
        (1, '被查看'),
        (2, '面试邀请'),
        (3, '录用'),
        (4, '不合适'),
    )

    # 关联三方：谁(seeker) -> 投了哪个职位(job) -> 用了哪份简历(resume)
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='求职者')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, verbose_name='申请职位')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='投递简历')

    status = models.SmallIntegerField(default=0, choices=STATUS_CHOICES, verbose_name='投递状态')
    hr_feedback = models.CharField(max_length=255, blank=True, verbose_name='HR反馈')

    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='投递时间')

    class Meta:
        verbose_name = '投递记录'
        verbose_name_plural = verbose_name