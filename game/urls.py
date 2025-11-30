from django.urls import path
from .views import home, course_detail, recommended_courses, register, login_view, logout_view, profile, edit_profile, add_course, all_reviews

urlpatterns = [
    path('', home, name='home'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('recommended/', recommended_courses, name='recommended'),
    path('reviews/', all_reviews, name='all_reviews'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('course/add/', add_course, name='add_course'),
]