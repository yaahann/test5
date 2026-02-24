from django.urls import path
from .views import ResumeListCreateView, ApplicationListCreateView,ResumeDetailView,RecruiterApplicationListView,ApplicationStatusUpdateView

urlpatterns = [
    # 简历接口: /api/recruitment/resumes/
    path('resumes/', ResumeListCreateView.as_view(), name='resume_list_create'),

    # 新增: 用于删除简历 /api/recruitment/resumes/1/
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),

    # 投递接口: /api/recruitment/applications/
    path('applications/', ApplicationListCreateView.as_view(), name='application_list_create'),

    path('recruiter/applications/', RecruiterApplicationListView.as_view(), name='recruiter_apps'),

    path('applications/<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='update_status'),
]