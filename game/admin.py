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
    list_display = ('name', 'platform', 'is_approved', 'created_by', 'created_at')
    search_fields = ('name', 'platform__name', 'created_by__username')
    list_filter = ('is_approved', 'platform', 'created_at')
    list_select_related = ('platform', 'created_by')
    actions = ['approve_courses', 'reject_courses']
    
    def approve_courses(self, request, queryset):
        """Одобрить выбранные курсы"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'Одобрено курсов: {updated}')
    approve_courses.short_description = "Одобрить выбранные курсы"
    
    def reject_courses(self, request, queryset):
        """Отклонить выбранные курсы"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'Отклонено курсов: {updated}')
    reject_courses.short_description = "Отклонить выбранные курсы"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'author_name', 'rating', 'created_at')
    search_fields = ('author_name', 'course__name')
    list_filter = ('rating', 'created_at')
    list_select_related = ('course',)
