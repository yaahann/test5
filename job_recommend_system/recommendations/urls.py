from django.urls import path
from .views import ContentBasedRecommendationView,CandidateRecommendationView

urlpatterns = [
    # 推荐列表接口：/api/recommendations/jobs/
    path('jobs/', ContentBasedRecommendationView.as_view(), name='recommend_jobs'),
    path('candidates/', CandidateRecommendationView.as_view(), name='recommend_candidates'),
]