from django.db import models


# [cite_start]8. 求职者行为日志 (对应文档 seeker_action_log) [cite: 131-132]
class SeekerActionLog(models.Model):
    ACTION_CHOICES = (
        (1, '浏览'),
        (2, '收藏'),
        (3, '投递'),
    )

    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='求职者')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, verbose_name='涉及职位')
    action_type = models.SmallIntegerField(choices=ACTION_CHOICES, verbose_name='行为类型')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='发生时间')

    class Meta:
        verbose_name = '求职者行为日志'
        verbose_name_plural = verbose_name


# [cite_start]9. 招聘者行为日志 (对应文档 recruiter_action_log) [cite: 133-134]
class RecruiterActionLog(models.Model):
    ACTION_CHOICES = (
        (1, '查看简历'),
        (2, '发起面试'),
    )

    recruiter = models.ForeignKey('users.Recruiter', on_delete=models.CASCADE, verbose_name='招聘者')
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='涉及求职者')
    action_type = models.SmallIntegerField(choices=ACTION_CHOICES, verbose_name='行为类型')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='发生时间')

    class Meta:
        verbose_name = '招聘者行为日志'
        verbose_name_plural = verbose_name


# [cite_start]10. 给求职者的职位推荐结果 (对应文档 seeker_recommendation) [cite: 135-136]
class SeekerRecommendation(models.Model):
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='求职者')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, verbose_name='推荐职位')

    match_score = models.FloatField(verbose_name='匹配度')
    recommend_rule = models.CharField(max_length=50, default='static', verbose_name='推荐规则')  # 静态/行为加权
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='计算时间')

    class Meta:
        verbose_name = '职位推荐结果'
        verbose_name_plural = verbose_name


# [cite_start]11. 给招聘者的人才推荐结果 (对应文档 recruiter_recommendation) [cite: 137-138]
class RecruiterRecommendation(models.Model):
    recruiter = models.ForeignKey('users.Recruiter', on_delete=models.CASCADE, verbose_name='招聘者')
    seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE, verbose_name='推荐人才')

    match_score = models.FloatField(verbose_name='匹配度')
    recommend_rule = models.CharField(max_length=50, default='static', verbose_name='推荐规则')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='计算时间')

    class Meta:
        verbose_name = '人才推荐结果'
        verbose_name_plural = verbose_name