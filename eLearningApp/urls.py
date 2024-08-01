from django.urls import path

from . import views

urlpatterns = [
    # View URL patterns
    path("", views.index, name="index"),
    path("features/", views.features, name="features"),
    path("login/", views.login, name="login"),
    path("enrol/", views.enrol, name="enrol"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("courses/", views.courses, name="courses"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("courses/details/<int:course_id>", views.courseDetails, name="courseDetails"),
    # API URL patterns
]