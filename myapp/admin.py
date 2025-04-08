from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser, UserAdmin)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_taken', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('student_name', 'course_taken')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill_level', 'duration', 'fee', 'instructor')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}  