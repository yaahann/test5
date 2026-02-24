from django.urls import path
from .views import JobListCreateView, JobDetailView,RecruiterJobListView,JobStatusUpdateView


urlpatterns = [
    # 职位列表 + 发布接口: /api/jobs/
    path('', JobListCreateView.as_view(), name='job_list_create'),

    # 职位详情 + 修改/删除接口: /api/jobs/1/
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),

    path('recruiter/my-jobs/', RecruiterJobListView.as_view(), name='recruiter_jobs'),

    path('<int:pk>/status/', JobStatusUpdateView.as_view(), name='job_status'),
]
