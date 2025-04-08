from django.db import models

# Create your models here.
class Job(models.Model):
    # Category choices
    CATEGORY_CHOICES = [
       ('software_dev', 'Software Development'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('networking', 'Networking & Infrastructure'),
        ('cloud_computing', 'Cloud Computing'),
        ('it_support', 'IT Support & Administration'),
        ('other', 'Other'),
    ]

    # Job type choices
    JOB_TYPE_CHOICES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    application_deadline = models.DateField()
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company}"
