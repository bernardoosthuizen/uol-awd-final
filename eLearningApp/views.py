# Import necessary modules
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
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
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        authenticated_user = authenticate(username=username, password=password)
        
        if authenticated_user is not None:
            if authenticated_user.is_active:
                auth_login(request, authenticated_user)
                return redirect('dashboard')
            else:
                return render(request,"login.html", {'error': 'Account is disabled.'})
        else:
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
     
    context = {
        "pageTitle": "Dashboard",
        "user_group": user_group,
    }
    return render(request, "dashboard.html", context)

@login_required
def courses(request):
    user_group = request.user.groups.first()
    
    context = {
        "pageTitle": "Courses",
        "user_group": user_group,
    }
    return render(request, "courses.html", context)

@login_required
def profile(request):
    context = {
        "pageTitle": "Profile",
    }
    return render(request, "profile.html", context)

@login_required
def courseDetails(request, course_id):
    user_group = request.user.groups.first()
    
    context = {
        "course_id": course_id,
        "pageTitle": "Course Details: " + str(id),
        "user_group": user_group
    }
    return render(request, "course-details.html", context)
