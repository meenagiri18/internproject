from django.urls import path
from .views import *

urlpatterns = [
    path('',instructor_dashboard,name='instructor_dashboard'),
    path('create_course',create_course,name='create_course'),
    path('my_courses',my_courses,name='my_courses'),
    path('edit_course/<int:course_id>',edit_course,name='edit_course'),
    path('view_course/<int:course_id>',view_course,name='view_course'),
    
]
