from rest_framework import generics, permissions
from jobs.models import Job
from jobs.serializers import JobSerializer

# 1. 职位推荐接口 (目前是假的，返回最新10个)
class JobRecommendationView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # TODO: 以后在这里接入真正的推荐算法 (基于 content-based 或协同过滤)
        # 目前逻辑：直接返回最新的、正在招聘的10个职位
        return Job.objects.filter(status=1).order_by('-create_time')[:10]