from django import forms
from .models import Review, UserProfile

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
