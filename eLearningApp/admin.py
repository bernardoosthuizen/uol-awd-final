from django.contrib import admin

# Register your models here.
from .models import *

class InstitutionAdmin(admin.ModelAdmin):
    model = Institution
    
class CourseAdmin(admin.ModelAdmin):
    model = Course
    
class AppUserAdmin(admin.ModelAdmin):
    model = AppUser
    
class CourseFeedbackAdmin(admin.ModelAdmin):
    model = CourseFeedback
    
class StudentStatusUpdateAdmin(admin.ModelAdmin):
    model = StudentStatusUpdate

class CourseEnrollmentAdmin(admin.ModelAdmin):
    model = CourseEnrollment

class CourseMaterialAdmin(admin.ModelAdmin):
    model = CourseMaterial
    
class CourseAssignmentAdmin(admin.ModelAdmin):
    model = CourseAssignment
    
    
    
    
    
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(CourseFeedback, CourseFeedbackAdmin)
admin.site.register(StudentStatusUpdate, StudentStatusUpdateAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)
admin.site.register(CourseAssignment, CourseAssignmentAdmin)

