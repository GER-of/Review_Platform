from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Platform, Course, Review, UserProfile
from .forms import ReviewForm, UserProfileForm, CourseSubmissionForm

def home(request):
    """Главная страница со списком всех курсов"""
    platform_filter = request.GET.get('platform')
    
    # Показываем только одобренные курсы
    if platform_filter:
        courses = Course.objects.filter(platform__id=platform_filter, is_approved=True).select_related('platform')
    else:
        courses = Course.objects.filter(is_approved=True).select_related('platform')
    
    platforms = Platform.objects.all()
    
    courses_with_ratings = []
    for course in courses:
        courses_with_ratings.append({
            'course': course,
            'avg_rating': course.average_rating()
        })
    
    return render(request, 'home.html', {
        'courses_with_ratings': courses_with_ratings,
        'platforms': platforms,
        'selected_platform': platform_filter
    })

def course_detail(request, course_id):
    """Страница детальной информации о курсе с отзывами"""
    course = get_object_or_404(Course.objects.select_related('platform'), id=course_id)
    reviews = course.reviews.select_related('user').all()
    avg_rating = course.average_rating()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Для добавления отзыва необходимо войти в систему.')
            return redirect('login')
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.author_name = request.user.username
            review.save()
            messages.success(request, 'Спасибо! Ваш отзыв успешно добавлен.')
            return redirect('course_detail', course_id=course.id)
    else:
        form = ReviewForm()
    
    return render(request, 'course_detail.html', {
        'course': course,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form
    })

def recommended_courses(request):
    """Страница рекомендуемых курсов (оценка выше 4.5)"""
    courses = Course.objects.filter(is_approved=True).select_related('platform')
    recommended = []
    for course in courses:
        avg_rating = course.average_rating()
        if avg_rating > 4.5:
            recommended.append({
                'course': course,
                'avg_rating': avg_rating
            })
    return render(request, 'recommended.html', {'recommended': recommended})

@login_required
def add_course(request):
    """Добавление курса пользователем"""
    if request.method == 'POST':
        form = CourseSubmissionForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.is_approved = False  # Требует одобрения администратора
            course.save()
            form.save_m2m()  # Сохраняем ManyToMany связи (категории)
            messages.success(request, 'Спасибо! Ваш курс отправлен на модерацию. После одобрения администратором он появится на сайте.')
            return redirect('home')
    else:
        form = CourseSubmissionForm()
    
    return render(request, 'add_course.html', {'form': form})

def all_reviews(request):
    """Страница со всеми отзывами"""
    reviews = Review.objects.select_related('course', 'course__platform', 'user').filter(course__is_approved=True).order_by('-created_at')
    
    return render(request, 'all_reviews.html', {
        'reviews': reviews
    })

def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def profile(request):
    """Профиль пользователя с его отзывами"""
    user_reviews = Review.objects.filter(user=request.user).select_related('course', 'course__platform')
    
    # Создаем профиль, если его нет
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.create(user=request.user)
    
    return render(request, 'profile.html', {
        'user_reviews': user_reviews
    })

@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    # Создаем профиль, если его нет
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {'form': form})