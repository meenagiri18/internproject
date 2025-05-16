from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('job_announcement',job_announcement,name='job_announcement'),
    path('profile',profile,name='profile'),
    path('apply_for_instructor',apply_for_instructor,name='apply_for_instructor'),
    path('enrolled_courses',enrolled_courses,name='enrolled_courses'),
    path('course/<int:course_id>/player/', course_player, name='course_player'),
]
