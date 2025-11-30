from django.contrib import admin
from .models import Platform, Course, Review, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'course_url', 'created_at')
    search_fields = ('name', 'platform__name')
    list_filter = ('platform', 'created_at')
    list_select_related = ('platform',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'author_name', 'rating', 'created_at')
    search_fields = ('author_name', 'course__name')
    list_filter = ('rating', 'created_at')
    list_select_related = ('course',)
