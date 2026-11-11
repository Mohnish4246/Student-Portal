from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(),name='student_detail'),
path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),
path(
    "skills/",
    views.SkillListView.as_view(),
    name="skill_list"
),
path(
    "courses/",
    views.CourseListView.as_view(),
    name="course_list"
),
path(
    "course/<int:pk>/",
    views.CourseDetailView.as_view(),
    name="course_detail"
),
path(
    "profile/",
    views.UserProfileView.as_view(),
    name="user_profile"
),
path(
    "skill/<int:pk>/",
    views.SkillDetailView.as_view(),
    name="skill_detail"
),
path(
    "statistics/",
    views.StudentStatisticsView.as_view(),
    name="student_statistics"
),
path(
    "course-statistics/",
    views.CourseStatisticsView.as_view(),
    name="course_statistics"
),
path(
    "top-students/",
    views.TopStudentsView.as_view(),
    name="top_students"
),
path(
    "popular-courses/",
    views.PopularCourseView.as_view(),
    name="popular_courses"
),
    path('about/', views.AboutView.as_view(),name='about'),
    path('contact/', views.contact,name='contact'),
    path('add/', views.add_student,name='add_student'),
    path('student/<int:id>/edit', views.edit_student,name='edit_student'),
    path('student/<int:id>/delete', views.delete_student,name='delete_student'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),
    path('register/', views.register,name='register'),
]