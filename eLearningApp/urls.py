from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("features/", views.features, name="features"),
    path("login/", views.login, name="login"),
    path("enrol/", views.enrol, name="enrol"),
]