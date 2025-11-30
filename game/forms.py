from django import forms
from .models import Review, UserProfile, Course

class ReviewForm(forms.ModelForm):
    """Форма для создания отзыва"""
    
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Расскажите о своем опыте прохождения курса...',
                'rows': 5
            }),
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Ваш отзыв'
        }

class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Расскажите о себе...',
                'rows': 4
            }),
        }
        labels = {
            'bio': 'О себе',
            'avatar': 'Аватар'
        }

class CourseSubmissionForm(forms.ModelForm):
    """Форма для добавления курса пользователем"""
    
    class Meta:
        model = Course
        fields = ['name', 'platform', 'categories', 'description', 'course_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Название курса'
            }),
            'platform': forms.Select(attrs={
                'class': 'form-input'
            }),
            'categories': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Подробное описание курса...',
                'rows': 5
            }),
            'course_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com/course'
            }),
        }
        labels = {
            'name': 'Название курса',
            'platform': 'Платформа',
            'categories': 'Категории',
            'description': 'Описание',
            'course_url': 'Ссылка на курс'
        }
        help_texts = {
            'course_url': 'Прямая ссылка на страницу курса',
            'categories': 'Выберите одну или несколько категорий'
        }
