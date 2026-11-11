from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, UserProfile, Skill
from .forms import StudentForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import View
from .decorators import admin_required
from django.db.models import Count, Avg, Min, Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

@login_required
def home(request):
    login_message = request.session.pop("login_message",None)
    search = request.GET.get("search","")
    marks_filter = request.GET.get("marks","")
    city_filter = request.GET.get("city","")

    students = Student.objects.filter(user=request.user)
    # name or city
    if search:
        students = students.filter(Q(name__icontains=search) | Q(city__icontains=search))

    # filter by marks
    if marks_filter == "80":
        students = students.filter(marks__gte=80)
    elif marks_filter == "60":
        students = students.filter(marks__gte=60)
    elif marks_filter == "below40":
        students = students.filter(marks__lt=40)
    # city filter
    if city_filter:
        students = students.filter(city=city_filter)
    cities = Student.objects.filter(user=request.user).values_list("city",flat=True).distinct()

    # pagination
    paginator = Paginator(students,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "students": page_obj,
        "search": search,
        "marks_filter": marks_filter,
        "city_filter": city_filter,
        "cities":cities,
        "login_message": login_message
    }
    return render(request,"home.html",context)

class AboutView(View):
    def get(self,request):
        return render(request,"about.html")

@admin_required
def admin_dashboard(request):

    students = Student.objects.all()

    return render(
        request,
        "admin_dashboard.html",
        {"students": students}
    )




# detail  view
class StudentDetailView(LoginRequiredMixin,DetailView):

    model = Student
    template_name = "student_detail.html"
    context_object_name = "student"

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

# Skill List View
class SkillListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = "skill_list.html"
    context_object_name = "skills"
    ordering = ["name"]

# Course List View
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"
    ordering = ["name"]
    
# course detail view
class CourseDetailView(LoginRequiredMixin,DetailView):

    model = Course
    template_name = "course_detail.html"
    context_object_name = "course"

# User Profile view
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "user_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(
            UserProfile,
            user=self.request.user
        )

# Skill Detail view

class SkillDetailView(LoginRequiredMixin, DetailView):
    model = Skill
    template_name = "skill_detail.html"
    context_object_name = "skill"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["students"] = self.object.students.filter(
            user=self.request.user
        )

        return context


# Student Statistics View
class StudentStatisticsView(LoginRequiredMixin, View):

    def get(self, request):

        students = Student.objects.filter(
            user=request.user
        )

        total_students = students.count()

        average_marks = students.aggregate(
            Avg("marks")
        )["marks__avg"]

        highest_marks = students.aggregate(
            Max("marks")
        )["marks__max"]

        lowest_marks = students.aggregate(
            Min("marks")
        )["marks__min"]

        context = {
            "total_students": total_students,
            "average_marks": average_marks,
            "highest_marks": highest_marks,
            "lowest_marks": lowest_marks,
        }

        return render(
            request,
            "student_statistics.html",
            context
        )


class CourseStatisticsView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course_statistics.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.annotate(
            student_count=Count(
                "students",
                filter=Q(students__user=self.request.user)
            )
        ).order_by("-student_count")

# 
class TopStudentsView(LoginRequiredMixin, ListView):

    model = Student
    template_name = "top_students.html"
    context_object_name = "students"

    def get_queryset(self):
        return Student.objects.filter(
            user=self.request.user,
            marks__gte=80
        ).order_by("-marks")



class PopularCourseView(LoginRequiredMixin, ListView):

    model = Course
    template_name = "popular_courses.html"
    context_object_name = "courses"

    def get_queryset(self):

        return Course.objects.annotate(
            student_count=Count("students",filter=Q(students__user=self.request.user))
        ).filter(
            Q(student_count__gte=2) |
            Q(name__icontains="Python")
        ).order_by(
            "-student_count"
        )









def contact(request):
    return render(request,"contact.html")


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            form.save_m2m()

            messages.success(
                request,
                "Student Added Successfully"
            )
            return redirect("home")
    else:
        form = StudentForm()

    return render(
        request,
        "add_student.html",
        {"form": form}
    )


@login_required
def edit_student(request,id):
    student = get_object_or_404(Student,id=id,user = request.user)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,"Student Edited Successfully")
            return redirect("home")
    else:
        form = StudentForm(instance=student)

    return render(request,"edit_student.html",{"form":form})

@login_required
def delete_student(request,id):
    student = get_object_or_404(Student,id=id,user=request.user)
    if request.method == "POST":
        student.delete()
        messages.success(request,"Student Deleted Successfully") # success, warning, error,info
        return redirect("home")
    return render(request,"delete_student.html",{"student":student})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            request.session["login_message"] = "Welcome back!"

            messages.success(request, "Login successful")

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)

            return redirect("home")

        messages.error(request, "Invalid username or password")

    return render(request, "login.html")



@login_required
@require_POST
def user_logout(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request,"register.html",{"form":form})