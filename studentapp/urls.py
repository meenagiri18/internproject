from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('job_announcement',job_announcement,name='job_announcement'),
    path('profile',profile,name='profile'),
    path('apply_for_instructor',apply_for_instructor,name='apply_for_instructor'),
]
