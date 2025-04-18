from django.shortcuts import render,redirect,get_object_or_404
from myapp.models import Course
from django.contrib import messages

# Create your views here.
def instructor_dashboard(request):
    return render(request,'instructor/instructordashboard.html')

def create_course(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        duration=request.POST.get('duration')
        skill_level = request.POST.get('skill_level')
        price = request.POST.get('price')
        prerequisite = request.POST.get('prerequisite')
        image = request.FILES.get('image')
        


        Course.objects.create(title=title,description=description,duration=duration,skill_level=skill_level,price=price,prerequisite=prerequisite,image=image,instructor=request.user)
        messages.success(request, "Course created successfully.")
        return redirect('course')
   
    return render(request,'instructor/create_course.html')

def my_courses(request):
    courses=Course.objects.filter(instructor=request.user)
    return render(request,'instructor/my_courses.html',{'courses':courses})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

   
    if course.instructor != request.user:
        return redirect('course')  

    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        course.skill_level = request.POST.get('skill_level')
        course.prerequisite = request.POST.get('prerequisite')
        course.price = request.POST.get('price')
        
        if request.FILES.get('image'):
            course.image = request.FILES['image']

        course.save()
        return redirect('course')  

    return render(request, 'instructor/edit_course.html', {'course': course})
def view_course(request, course_id):
   
    course = get_object_or_404(Course, id=course_id)
    
    return render(request, 'instructor/view_course.html', {'course': course})


