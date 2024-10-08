# --- URLS ---
# Defines URL patterns.

# Importing necessary modules
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from . import views
from . import api

urlpatterns = [
    # View URL patterns
    path("", views.index, name="index"),
    path("features/", views.features, name="features"),
    path("login/", views.login, name="login"),
    path("enrol/", views.enrol, name="enrol"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("timeline/", views.timeline, name="timeline"),
    path("courses/", views.courses, name="courses"),
    path("students/", views.students, name="students"),
    path("user/<int:user_id>", views.user, name="user"),
    path("chats/", views.chats, name="chats"),
    path("chat/<str:chat_id>", views.chatroom, name="chatroom"),
    path("start_chat/<int:teacher_id>/<int:student_id>", views.start_chat, name="start_chat"),
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
    # Schema urls
    path("apischema/", get_schema_view(
        title='Coursify REST API', 
        description="API for interacting with user records",
        version='1.0'), name="openapi-schema"),
    path("api-docs/", TemplateView.as_view(
        template_name='api-docs.html',
        extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),
    # API URL patterns
    path("api/users/", api.users, name='api_users'),
    path("api/user/<int:user_id>", api.user, name='api_user'),
    path("api/file/", api.file, name='api_file'),
]