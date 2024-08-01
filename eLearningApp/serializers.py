# Import necessary modules
from rest_framework import serializers
from .models import *

# Institution serializer
class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        
# Course serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
# AppUser serializer
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
        
# Course feedback serializer
class CourseFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeedback
        fields = '__all__'
        
# Student status update serializer
class StudentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatusUpdate
        fields = '__all__'
        
# Course enrollment serializer
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        
# Course material serializer
class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = '__all__'
        
# Course assignment serializer
class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = '__all__'
        