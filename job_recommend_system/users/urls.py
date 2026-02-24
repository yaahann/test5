from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
# 确保这里引入了 MyTokenObtainPairView 和 JobSeekerDetailView
from .views import RegisterView, MyTokenObtainPairView, JobSeekerDetailView
from .views import PublicCompanyListView, RecruiterDetailView,PublicCompanyDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('seeker/profile/', JobSeekerDetailView.as_view(), name='seeker_profile'),
    path('companies/', PublicCompanyListView.as_view(), name='public_companies'),
    path('recruiter/profile/', RecruiterDetailView.as_view(), name='recruiter-profile'),
    path('companies/<int:pk>/', PublicCompanyDetailView.as_view(), name='public-company-detail'),
]