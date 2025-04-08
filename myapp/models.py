from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE = (
        ("student", "Student"),
        ("instructor", "Instructor"),
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE)
    instructor_applied = models.BooleanField(default=False)
    instructor_approved = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    user_profile_image = models.ImageField(upload_to="images/profile_images/")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    

class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    course_taken = models.CharField(max_length=100, help_text="Course the student took")
    testimonial = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 and 5"
    )
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.course_taken}"
    
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    DURATION_CHOICES = [
        ('short-term', 'Short-term'),
        ('long-term', 'Long-term'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    
    CATEGORIES = [
        ('trends', 'IT Industry Trends'),
        ('learning-tips', 'Learning Tips for Programming'),
        ('career-guidance', 'Career Guidance in Tech Fields'),
    ]

    # Fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='trends')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})    