import re
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def base(request):
    return render(request,'base.html')
def home(request):
    testimonials = Testimonial.objects.all()
    testimonial_groups = [testimonials[i:i + 3] for i in range(0, len(testimonials), 3)]

    context = {
        'testimonials': testimonial_groups,
    }
    return render(request, 'main/home.html', context)
    
def course(request):
    courses = Course.objects.all()
    instructors = Instructor.objects.all()
    context = {
        'courses': courses,
        'instructors': instructors,
    }

    return render(request,'main/courses.html',context)

def about(request):
    return render(request,'main/about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['number']
        message=request.POST['message']
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            messages.error(request, "Invalid email")
            return redirect("contact")
        else:
            Contact.objects.create(name=name,email=email,phone=phone,message=message)
            subject="Form Submission"
            message="formm"
            from_email="meenagiri2058@gmail.com"
            recipient_list="meenagiri2058@gmail.com"
            send_mail(subject,message,from_email,recipient_list,fail_silently=True)

            messages.success(request,f'Hi {name} your form is successfully submit')
            return redirect('home')

    return render(request,'main/contact.html')
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'main/blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'main/blog_detail.html', {'blog': blog})
def log_in(request):
  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')  # Success message
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')  # Error message
   
            
    return render(request,'auth/login.html')

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']

        # Check if passwords match
        if password != password1:
            messages.error(request, 'Passwords do not match.')  # Error message
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')  # Error message
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')  # Error message
            return redirect('register')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Registration successful. Please log in.')  # Success message
        return redirect('login')
    else:
         return render(request,'auth/register.html')
    
def log_out(request):
    logout(request)  
    messages.success(request, 'You have been successfully logged out.')  # Success message
    return redirect('home')   
           

   
