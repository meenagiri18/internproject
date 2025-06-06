from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE = (
        ("student", "Student"),
        ("instructor", "Instructor"),
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default='student')
    instructor_applied = models.BooleanField(default=False)
    instructor_approved = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    user_profile_image = models.ImageField(upload_to="images/profile_images/")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    enrolled_courses = models.ManyToManyField('Course', related_name='enrolled_users', blank=True)

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
    instructor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,  
    blank=True, 
    related_name='courses'
)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    prerequisite = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='course_thumbnails/')
    promo_video_url = models.URLField(max_length=350, blank=True, null=True, help_text="YouTube/Vimeo embed URL")
    syllabus_video = models.FileField(upload_to='course_videos/', blank=True, null=True, 
                                   help_text="Upload video file if not using URL")
    syllabus_text = models.TextField(blank=True, help_text="Detailed course syllabus")
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


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("esewa", "eSewa"),
        ("khalti", "Khalti")
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    purchase_order_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # <-- Add this line
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):  # You had a typo: use __str__, not str
        return f"{self.user.username} - {self.course.title} - {self.payment_method} - {self.status}"



class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

    def str(self):
        return f"{self.student.username} enrolled in {self.course.title}"           