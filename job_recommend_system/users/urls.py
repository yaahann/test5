from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, MyTokenObtainPairView, JobSeekerDetailView,RecruiterDetailView
from .views import (PublicCompanyListView,PublicCompanyDetailView,
                    AdminPendingRecruitersView,AdminAuditRecruiterView,AdminStatsView,AdminAllSeekersView,AdminAllRecruitersView,
                    SendMessageView,MyMessagesView,MarkMessageReadView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('seeker/profile/', JobSeekerDetailView.as_view(), name='seeker_profile'),
    path('recruiter/profile/', RecruiterDetailView.as_view(), name='recruiter-profile'),
    path('companies/', PublicCompanyListView.as_view(), name='public_companies'),
    path('companies/<int:pk>/', PublicCompanyDetailView.as_view(), name='public-company-detail'),
    path('admin/recruiters/pending/', AdminPendingRecruitersView.as_view()),
    path('admin/recruiters/<int:pk>/audit/', AdminAuditRecruiterView.as_view()),
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('admin/seekers/all/', AdminAllSeekersView.as_view()),
    path('admin/recruiters/all/', AdminAllRecruitersView.as_view()),
    path('messages/send/', SendMessageView.as_view(), name='send_message'),
    path('messages/my/', MyMessagesView.as_view(), name='my_messages'),
    path('messages/<int:pk>/read/', MarkMessageReadView.as_view(), name='mark_message_read'),
]