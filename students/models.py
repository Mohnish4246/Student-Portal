from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    fees = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserQuerySet(models.QuerySet):
    def for_user(self,user):
        return self.filter(user=user)
    def passed(self):
        return self.filter(marks__gte=40)
    def top_students(self):
        return self.filter(marks__gte=80).order_by("-marks")

class Student(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students" # course.students.all()
    )
    skills = models.ManyToManyField(
        Skill,
        blank = True,           
        related_name="students" # skills.students.all() = Aman,Ankit,Siya ; student.skills.all() = Python,SQL...
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="", blank=True)
    marks = models.IntegerField()
    city = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to="student_images/",
        blank=True,
        null = True
    )
    document = models.FileField(upload_to="student_documents/",blank=True,null=True) # student.document.url = media/student_documents/resume.pdf
    objects = UserQuerySet.as_manager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(marks__gte=0) & Q(marks__lte=100),
                name="student_marks_0_to_100",
            ),
            models.UniqueConstraint(
                fields=["user","email"],
                name="unique_student_email_per_user",
            )
        ]

    def clean(self):
        if self.marks < 0 or self.marks > 100:
            raise ValidationError(
                "Marks must be between 0 and 100."
            )


    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True,blank=True)
    address = models.TextField(blank=True)
    guardian_name = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

