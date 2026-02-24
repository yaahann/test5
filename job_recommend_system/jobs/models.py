from django.db import models
from django.conf import settings  # 引用我们自定义的用户模型


# 5. 职位表 (对应文档中的 job 表)
class Job(models.Model):
    # 关联招聘者 (recruiter_id) [cite: 126]
    # 注意：这里我们关联到 users 应用里的 Recruiter 模型
    recruiter = models.ForeignKey('users.Recruiter', on_delete=models.CASCADE, verbose_name='发布企业')

    job_title = models.CharField(max_length=100, verbose_name='职位名称')
    job_type = models.CharField(max_length=20, verbose_name='职位类型',
                                choices=(('全职', '全职'), ('实习', '实习'), ('兼职', '兼职')))
    city = models.CharField(max_length=50, verbose_name='工作城市')

    # 薪资通常存整数，单位可以是 k/月
    salary_min = models.IntegerField(verbose_name='最低薪资(k)')
    salary_max = models.IntegerField(verbose_name='最高薪资(k)')

    education_req = models.CharField(max_length=20, verbose_name='学历要求', default='不限')
    exp_req = models.CharField(max_length=20, verbose_name='经验要求', default='不限')

    # 核心字段：职位标签，用于推荐算法 [cite: 126]
    job_tags = models.CharField(max_length=255, verbose_name='职位标签', help_text='用于匹配度计算，如: Python,后端')

    description = models.TextField(verbose_name='职位描述')

    # 状态管理
    status = models.SmallIntegerField(default=0, verbose_name='职位状态',
                                      choices=((0, '待审'), (1, '招聘中'), (2, '已下架')))

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '职位信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_title


# 7. 职位收藏表 (对应文档中的 job_collection 表) [cite: 129-130]
class JobCollection(models.Model):
    # 关联求职者
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='求职者')
    # 关联职位
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='收藏职位')

    collect_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '职位收藏'
        verbose_name_plural = verbose_name
        # 联合唯一索引，防止重复收藏同一个职位
        unique_together = ('seeker', 'job')