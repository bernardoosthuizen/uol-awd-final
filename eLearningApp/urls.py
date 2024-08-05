from django.urls import path, re_path

from . import views
from . import api

urlpatterns = [
    # View URL patterns
    path("", views.index, name="index"),
    path("features/", views.features, name="features"),
    path("login/", views.login, name="login"),
    path("enrol/", views.enrol, name="enrol"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("courses/", views.courses, name="courses"),
    path("students/", views.students, name="students"),
    path("profile/", views.profile, name="profile"),
    path("courses/details/<int:course_id>", views.courseDetails, name="courseDetails"),
    path("logout/", views.user_logout, name="logout"),
    path("update_status/", views.update_status, name="update_status"),
    path("give_feedback/<int:course_id>", views.give_feedback, name="give_feedback"),
    path("create_course/", views.create_course, name="create_course"),
    path("create_assignment/<int:course_id>", views.create_assignment, name="create_assignment"),
    path("join_course/<int:course_id>", views.join_course, name="join_course"),
    path("delete_profile/", views.delete_profile, name="delete_profile"),
    path("remove_enrolment/<int:course_id>/<int:student_id>", views.remove_enrolment, name="remove_enrolment"),
    path("api/", views.api, name="api"),
    # API URL patterns
    path("api/users/", api.users, name='api_users'),
    re_path(r"^api/user(?:/(?P<pk>\d+))?$", api.user, name='api_user'),
]