from django.contrib import admin
from .models import SeekerRecommendation, RecruiterRecommendation
# 日志表通常数据量大，仅注册用于调试，或者不注册也可以
admin.site.register(SeekerRecommendation)
admin.site.register(RecruiterRecommendation)