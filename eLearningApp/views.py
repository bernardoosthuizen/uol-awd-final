# Import necessary modules
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
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
        user_form = UserForm(request.POST)
        profile_form = AppUserForm(request.POST)
        
        
        if user_form.is_valid() and profile_form.is_valid():
            # Check if passwords match
            if user_form.cleaned_data['password1'] != user_form.cleaned_data['password2']:
                user_form.add_error('password1', "Passwords do not match.")
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
            
            enrolled = True
            
            return redirect('dashboard')
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

def dashboard(request):
    context = {
        "pageTitle": "Dashboard",
    }
    return render(request, "dashboard.html", context)

def courses(request):
    context = {
        "pageTitle": "Courses",
    }
    return render(request, "courses.html", context)

def profile(request, user_id):
    context = {
        "user_id": user_id,
        "pageTitle": "Profile",
    }
    return render(request, "profile.html", context)

def courseDetails(request, course_id):
    context = {
        "course_id": course_id,
        "pageTitle": "Course Details: " + str(id),
    }
    return render(request, "course-details.html", context)
