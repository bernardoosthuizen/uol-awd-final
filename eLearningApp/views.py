from django.shortcuts import render
from django.http import HttpResponse


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
    context = {
        "pageTitle": "Enrol",
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

def profile(request):
    context = {
        "pageTitle": "Profile",
    }
    return render(request, "profile.html", context)


