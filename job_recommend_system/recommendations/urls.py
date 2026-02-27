from django.urls import path
from .views import ContentBasedRecommendationView

urlpatterns = [
    # 推荐列表接口：/api/recommendations/jobs/
    path('jobs/', ContentBasedRecommendationView.as_view(), name='recommend_jobs'),
]