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
    path("profile/", views.profile, name="profile"),
    path("courses/details/<int:course_id>", views.courseDetails, name="courseDetails"),
    path("logout/", views.user_logout, name="logout"),
    path("update_status/", views.update_status, name="update_status"),
    path("give_feedback/<int:course_id>", views.give_feedback, name="give_feedback"),
    path("create_course/", views.create_course, name="create_course"),
    path("create_assignment/<int:course_id>", views.create_assignment, name="create_assignment"),
    path("join_course/<int:course_id>", views.join_course, name="join_course"),
    # API URL patterns
]