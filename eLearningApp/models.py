# --- MODELS ---
# Defining database schemas.

# Import necessary modules
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
# Course feedback model
class CourseFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.course.name
    
    def save(self, *args, **kwargs):
        appUser = AppUser.objects.get(user=self.user)
        # Check if user and course are part of the same institution
        if appUser.institution != self.course.institution:
            raise ValidationError("User and course must be part of the same institution.")
        
        # Check if user is enrolled in the course
        if not CourseEnrollment.objects.filter(user=self.user, course=self.course).exists():
            raise ValidationError("User must be enrolled in the course to provide feedback.")
        
        super().save(*args, **kwargs)
    
# Student status updte model
class StudentStatusUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username
    
# Course enrollment model
class CourseEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.course.name
    
    def save(self, *args, **kwargs):
        appUser = AppUser.objects.get(user=self.user)
        if appUser.institution != self.course.institution:
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
    
# Course assignment model
class CourseAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Check if deadline is in the future
        if self.deadline < datetime.date.today():
            raise ValidationError("Deadline must be in the future.")
        super().save(*args, **kwargs)
        
# Nofiication model
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    for_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        if self.receiving_user is not None and self.for_course is not None:
            raise ValidationError("Notification must be for a user or a course, not both.")
        if self.receiving_user is None and self.for_course is None:
            raise ValidationError("Notification must be for a user or a course.")
        super().save(*args, **kwargs)
        
# Chats model
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    
    def __str__(self):
        return self.teacher.username + "-" + self.student.username
    
    def save(self, *args, **kwargs):
        if self.teacher == self.student:
            raise ValidationError("Users must be different.")
        super().save(*args, **kwargs)
        
# Upladed Images model
class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    file = models.FileField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.file.url