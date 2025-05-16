from django.utils import timezone
import re
import uuid
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
import requests
from .models import *
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
KHALTI_SECRET_KEY = "4d6e32adf07a4c8e962c857654f0c956"
KHALTI_INITIATE_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"

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
    
    skill_level = request.GET.get('skillLevel')
    duration = request.GET.get('duration')
    price_range = request.GET.get('priceRange')

    courses = Course.objects.all()

    # Apply skill level filter
    if skill_level and skill_level != 'Skill Level':
        courses = courses.filter(skill_level=skill_level)

    # Apply duration filter
    if duration and duration != 'Duration':
        courses = courses.filter(duration=duration)

    # Apply price sorting
    if price_range == 'low':
        courses = courses.order_by('price')
    elif price_range == 'high':
        courses = courses.order_by('-price')

    instructors = Instructor.objects.all()

    context = {
        'courses': courses,
        'instructors': instructors,
    }

    return render(request, 'main/courses.html', context)
def about(request):
    return render(request,'main/about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['number']
        message=request.POST['message']
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", email):
            messages.error(request, "Invalid email")
            return redirect("contact")
        else:
            try:
                email_message = EmailMessage(
                subject='Form submission',
                body='Hi {name} your form has been successfully submitted.Wait for the response from the company.Thankyou!!!',
                from_email="meenagiri2058@gmail.com",  
                to=["meenagiri2058@gmail.com"], 
                headers={"Reply-To": email}  
            )
                email_message.send(fail_silently=False)
                messages.success(request, "Email has been sent!!")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
                return redirect("contact")


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
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')  # Error message
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')  # Error message
            return redirect('register')

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Registration successful. Please log in.')  # Success message
        return redirect('log_in')
    else:
         return render(request,'auth/register.html')
    
def log_out(request):
    logout(request)  
    messages.success(request, 'You have been successfully logged out.')  # Success message
    return redirect('home')  

def payment(request ,id):
    course=Course.objects.get(id=id)
    transaction_id = uuid.uuid4().hex
    return render(request, 'main/payment.html', {'course':course, 'transaction_id':transaction_id})

def initkhalti(request):
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        purchase_order_id = request.POST.get("purchase_order_id")
        amount = int(float(request.POST.get("amount")) * 100) 
        course_id = request.POST.get("course_id")

        request.session["course_id"] = course_id

        course = get_object_or_404(Course, id=course_id)
        user = request.user

     
        Payment.objects.create(
            user=user,
            course=course,
            amount=amount / 100, 
            payment_method='khalti',
            purchase_order_id=purchase_order_id,
            status='pending'
        )

        return_url = request.build_absolute_uri(reverse("payment_success"))

        payload = {
            "return_url": return_url,
            "website_url": request.build_absolute_uri("/"),
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "Course Payment",
        }

        headers = {"Authorization": f"Key {KHALTI_SECRET_KEY}"}

        response = requests.post(KHALTI_INITIATE_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and "payment_url" in response_data:
            khalti_payment_url = response_data["payment_url"]
            return redirect(khalti_payment_url)
        else:
            return JsonResponse({"error": "Khalti Payment Failed"}, status=400)

    return redirect("courses")

def payment_success(request):
    transaction_id = request.GET.get('transaction_id') 
    amount = request.GET.get('amount')
    purchase_order_id = request.GET.get('purchase_order_id')
    
    payment = get_object_or_404(Payment, purchase_order_id=purchase_order_id)
    course = payment.course

    payment.transaction_id = transaction_id
    payment.status = "completed"
    payment.save()

    if course not in request.user.enrolled_courses.all():
        request.user.enrolled_courses.add(course)
    
    context = {
        'course': course,
        'amount': amount,
        'transaction_id': transaction_id,
        'payment_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render(request, 'main/payment_success.html', context)


def payment_failure(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    error_message = request.GET.get('error_message', 'Payment processing failed')
    transaction_id = request.GET.get('transaction_id', 'N/A')
    amount = request.GET.get('amount', '0')

    context = {
        'course': course,
        'error_message': error_message,
        'transaction_id': transaction_id,
        'amount': amount,
    }
    return render(request, 'main/payment_failure.html', context)
   
