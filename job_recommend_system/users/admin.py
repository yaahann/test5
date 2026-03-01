from django.contrib import admin
from .models import User, JobSeeker, Recruiter,Message

admin.site.register(User)
admin.site.register(JobSeeker)
admin.site.register(Recruiter)
admin.site.register(Message)