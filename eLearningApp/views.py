# --- VIEWS ---
# Backend funstions for each page.

# Import necessary modules
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from .models import *
from .forms import *


def index(request):
    context = {
        "pageTitle": "Home",
    }
    return render(request, "index.html", context)

def features(request):
    context = {
        "pageTitle": "Features",
    }
    return render(request, "features.html", context)

def login(request):
    # Chech if its a POST request
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate user
        authenticated_user = authenticate(username=username, password=password)
        
        if authenticated_user is not None:
            # If user is authenticated and active log them in
            if authenticated_user.is_active:
                auth_login(request, authenticated_user)
                return redirect('dashboard')
            else:
                # Display error if account is disabled
                return render(request,"login.html", {'error': 'Account is disabled.'})
        else:
            # Display error if login credentials are invalid
            return render(request,"login.html", {'error': 'Invalid login credentials.'})
        
        
    context = {
        "pageTitle": "Login",
    }
    return render(request, "login.html", context)

def enrol(request):
    # Get names of all institutions
    institutions = Institution.objects.all()
    institution_list = [{'id': institution.id, 'name': institution.name} for institution in institutions]
    
    enrolled = False
    
    if request.method == "POST":
        # Get form data
        user_form = UserForm(request.POST)
        profile_form = AppUserForm(request.POST)
        
        
        if user_form.is_valid() and profile_form.is_valid():
            # Check if passwords match
            if user_form.cleaned_data['password1'] != user_form.cleaned_data['password2']:
                user_form.add_error(None, "Passwords do not match.")
                return render(request, "enrol.html", {"user_form": user_form, "profile_form": profile_form, "institutions": institution_list})
            # Save the user
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            # Add user to the student group
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)
            # Save the institution to the user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            institution_id = request.POST.get('institution')
            profile.institution = Institution.objects.get(id=institution_id)
            profile.save()
            
            # Log the user in
            authenticated_user = authenticate(username=user.username, password=user_form.cleaned_data['password1'])
            
            if authenticated_user is not None:
                if authenticated_user.is_active:
                    auth_login(request, authenticated_user)
                    return redirect('dashboard')
                else:
                    user_form.add_error(None, "Account is disabled.")
                    return render(request, "enrol.html", {"user_form": user_form, "profile_form": profile_form, "institutions": institution_list})
            else: 
                user_form.add_error(None, "Invalid login.")
                return render(request, "enrol.html", {"user_form": user_form, "profile_form": profile_form, "institutions": institution_list})
            
            enrolled = True
            
            
    else:
        user_form = UserForm()
        profile_form = AppUserForm()
        
    
    context = {
        "institutions": institutions,
        "pageTitle": "Enrol",
        "user_form": user_form,
        "profile_form": profile_form,
        "enrolled": enrolled,
    }
    return render(request, "enrol.html", context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    user_group = request.user.groups.first()
    # Get status updates of the user
    status_updates = StudentStatusUpdate.objects.filter(user=request.user).order_by('-date')[:5]
    
    # find enrolled courses
    course_enrollments = CourseEnrollment.objects.filter(user=request.user)
    enrolled_courses = Course.objects.filter(id__in=course_enrollments.values('course_id'))[:5]
    
    # get deadlines
    course_deadlines = CourseAssignment.objects.filter(course__in=enrolled_courses).order_by('-deadline')
    
    # get notifications
    user_notifications = Notification.objects.filter( Q(receiving_user=request.user) | Q(for_course__in=enrolled_courses)).order_by('-date')[:10]
    
    context = {
        "pageTitle": "Dashboard",
        "user_group": user_group,
        "status_updates": status_updates,   
        "enrolled_courses": enrolled_courses,
        "course_deadlines": course_deadlines,
        "user_notifications": user_notifications,
    }
    
    return render(request, "dashboard.html", context)

@login_required
def courses(request):
    user_group = request.user.groups.first()
    # find enrolled courses
    course_enrollments = CourseEnrollment.objects.filter(user=request.user)
    enrolled_courses = Course.objects.filter(id__in=course_enrollments.values('course_id'))
    
    all_courses = Course.objects.filter(institution=AppUser.objects.get(user=request.user).institution)
    
        
    context = {
        "pageTitle": "Courses",
        "user_group": user_group,
        "enrolled_courses": enrolled_courses,
        "all_courses": all_courses, 
    }
    return render(request, "courses.html", context)

@login_required
def students(request):
    # Get students only from current institution.
    institution = AppUser.objects.get(user=request.user).institution
    students = AppUser.objects.filter(institution=institution)
    student_details = User.objects.filter(id__in=students.values('user_id'))
    user_group = request.user.groups.first()
    teacher_id = request.user.id
    
    context = {
        "pageTitle": "Students",
        "students": student_details,
        "institution": institution, 
        "user_group": user_group,
        "teacher_id": teacher_id,
    }
    return render(request, "students.html", context)

@login_required
def chats(request):
    user_group = request.user.groups.first()
    open_chats = Chat.objects.filter(Q(teacher=request.user) | Q(student=request.user))
    context = {
        "pageTitle": "Chats",
        "user_group": user_group,
        "open_chats": open_chats,
    }
    return render(request, "chats.html", context)

@login_required
def chatroom(request, chat_id):
    user_group = request.user.groups.first()
    teacher_id, student_id = chat_id.split('-')
    teacher = User.objects.get(id=teacher_id)
    student = User.objects.get(id=student_id)
    
    context = {
        "pageTitle": "Chatroom",
        "user_group": user_group,
        "chat_id": chat_id,
        "teacher": teacher,
        "student": student,
    }
    return render(request, "chatroom.html", context)

@login_required
def profile(request):
    user_group = request.user.groups.first()
    context = {
        "pageTitle": "Profile",
        "user_group": user_group,
    }
    return render(request, "profile.html", context)

@login_required
def courseDetails(request, course_id):
    user_group = request.user.groups.first()
    
    course = Course.objects.get(id=course_id)
    
    course_deadlines = CourseAssignment.objects.filter(course=course)
    course_materials = CourseMaterial.objects.filter(course=course)
    course_feedback = CourseFeedback.objects.filter(course=course)
    enrolled_students = CourseEnrollment.objects.filter(course=course)
    course_students = User.objects.filter(id__in=enrolled_students.values('user_id'))

    context = {
        "course": course,
        "pageTitle": "Course Details: " + str(course),
        "user_group": user_group,
        "course_deadlines": course_deadlines,
        "course_materials": course_materials,
        "course_feedback": course_feedback, 
        "course_students": course_students,
        
    }
    return render(request, "course-details.html", context)

@login_required
def update_status(request):
    if request.method == "POST":
        # Get new status
        status = request.POST.get('status_update')
        
        # Write status to database
        user = request.user
        status_update = StudentStatusUpdate(user=user, status=status)
        status_update.save()
        
        return redirect('dashboard')
    
@login_required
def give_feedback(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(id=course_id)
        # Get feedback from form
        feedback = request.POST.get('feedback')
        # Write feedback to database
        course_feedback = CourseFeedback(course=course, user=request.user, feedback=feedback)
        course_feedback.save()
        
        return redirect('courseDetails', course_id)

@login_required
def create_course(request):
    if request.method == "POST":
        # Save course
        course_name = request.POST.get('name')
        institution = AppUser.objects.get(user=request.user).institution
        institution_obj = Institution.objects.get(name=institution)
        Course.objects.create(name=course_name, lecturer=request.user, institution=institution_obj)
        
        # Enroll lecturer in course
        course = Course.objects.get(name=course_name)
        CourseEnrollment.objects.create(user=request.user, course=course)
        
        return redirect('courses')
        
    else:
        course_form = CourseForm()
        
    context = {
        "pageTitle": "Create Course",
        "course_form": course_form,
    }
    
    return render(request, "create-course.html", context)


@login_required
def create_assignment(request, course_id):
    if request.method == "POST":
        # Save assignment
        course = Course.objects.get(id=course_id)
        assignment_name = request.POST.get('title')
        deadline_str = request.POST.get('due_date')
        deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date() # Convert into date object
        description = request.POST.get('description')
        CourseAssignment.objects.create(course=course, title=assignment_name, deadline=deadline, description=description)
        
        return redirect('courseDetails', course_id)
        
    else:
        course_id = request.GET.get('course_id')
        course = Course.objects.get(id=course_id)
        
        context = {
            "pageTitle": "Create Assignment",
            "course": course,
        }
        
        return render(request, "create-assignment.html", context)

@login_required
def join_course(request, course_id):
    course = Course.objects.get(id=course_id)
    # Add enrollment
    CourseEnrollment.objects.create(user=request.user, course=course)
    # Add notification
    Notification.objects.create(receiving_user=course.lecturer, message=request.user.first_name + " " + request.user.last_name + " has enrolled in " + course.name)
    
    return redirect('courses')

@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    return redirect('index')

@login_required
def remove_enrolment(request, course_id, student_id):
    if request.method == "POST":
        # Get student to remove.
        course = Course.objects.get(id=course_id)
        student_user = User.objects.get(id=student_id)
        # get the relatevent enrollment
        enrollment = CourseEnrollment.objects.get(user=student_user, course=course)
        # unenroll student
        enrollment.delete()
        
        return redirect('courses')
    
@login_required
def start_chat(request, teacher_id, student_id):
    if request.method == "GET":
        # Get student to chat with
        student_user = User.objects.get(id=student_id)
        teacher_user = User.objects.get(id=teacher_id)
        chat = Chat.objects.filter(Q(teacher=teacher_user) & Q(student=student_user))
        if chat:
            return redirect('chatroom', str(teacher_user.id) + '-' + str(student_user.id))
        else:
            # create chat if it does not exist
            chat = Chat.objects.create(teacher=teacher_user, student=student_user)
        
        return redirect('chatroom', str(teacher_user.id) + '-' + str(student_user.id))