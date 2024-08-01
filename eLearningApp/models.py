# Import necessary modules
from django.db import models
from django.contrib.auth.models import User

# Institution model
class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Courses model
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Extend the User model
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
# Course feedback model
class CourseFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.course.name
    
    def save(self, *args, **kwargs):
        # Check if user and course are part of the same institution
        if self.user.institution != self.course.institution:
            raise ValidationError("User and course must be part of the same institution.")
        
        # Check if user is enrolled in the course
        if not CourseEnrollment.objects.filter(user=self.user, course=self.course).exists():
            raise ValidationError("User must be enrolled in the course to provide feedback.")
        
        super().save(*args, **kwargs)
    
# Student status updte model
class StudentStatusUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username
    
# Course enrollment model
class CourseEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username
    
    def save(self, *args, **kwargs):
        if self.user.institution != self.course.institution:
            raise ValidationError("User and course must be part of the same institution.")
        super().save(*args, **kwargs)
        
# Course material model
class CourseMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='course_materials/')
    
    def __str__(self):
        return self.title