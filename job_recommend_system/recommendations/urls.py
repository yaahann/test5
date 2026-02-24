from django.urls import path
from .views import JobRecommendationView

urlpatterns = [
    # 推荐给求职者的职位: /api/recommendations/jobs/
    path('jobs/', JobRecommendationView.as_view(), name='recommend_jobs'),
]