from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from myapp.models import Course
from myapp.models import Payment
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def job_announcement(request):
    jobs= Job.objects.all()
    return render(request,'dashboard/job_announcement.html',{'jobs':jobs})

def profile(request):
    return render(request,"dashboard/profile.html",{'user':request.user})

from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect

def apply_for_instructor(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to apply as an instructor.")
        return redirect('log_in')
    
    if request.method == 'POST':
        try:
            # Check if already applied
            if request.user.instructor_applied:
                messages.info(request, "You've already submitted an instructor application.")
                return redirect('dashboard')
            
            # Prepare email content
            subject = f'New Instructor Application: {request.user.username}'
            message = (
                f'User Details:\n'
                f'Name: {request.user.get_full_name()}\n'
                f'Username: {request.user.username}\n'
                f'Email: {request.user.email}\n\n'
                f'Please review this application in the admin panel.'
            )
            
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email='meenagiri2058@gmail.com',
                to='meenagiri2058@gmail.com', 
                reply_to=[request.user.email]
            )
            
            # Send email
            email_message.send(fail_silently=False)
            
            # Update user status
            request.user.instructor_applied = True
            request.user.save()
            
            messages.success(
                request,
                "Your instructor application has been submitted successfully! "
                "Our team will review your request and contact you soon."
            )
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(
                request,
                "We couldn't process your request right now. "
                "Please try again later or contact support."
            )
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Instructor application error: {str(e)}", exc_info=True)
            return redirect('dashboard')
    
    return redirect('dashboard')

def enrolled_courses(request):
    payments = Payment.objects.filter(user=request.user, status='completed')
    enrolled_courses = [payment.course for payment in payments]
    return render(request, 'dashboard/enrolled_course.html', {'courses': enrolled_courses})

def course_player(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    
    enrolled_courses = Payment.objects.filter(user=request.user, status='completed').values_list('course_id', flat=True)
    if course.id not in enrolled_courses:
        return redirect('enrolled_courses')

    return render(request, 'dashboard/course_player.html', {
        'course': course,
        'enrolled': True
    })



