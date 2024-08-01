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
