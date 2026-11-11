from django.contrib import admin
from .models import Student, Course, UserProfile, Skill

# Username = abc
# Password = 123
# Register your models here.
# admin.site.register(Student)
admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(Skill)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "age",
        "email",
        "phone",
        "marks",
        "city",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "city",
    )

    list_filter = (
        "city",
    )

    ordering = (
        "-marks",
    )