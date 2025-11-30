from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    bio = models.TextField(verbose_name="О себе", blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватар", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"Профиль {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматическое создание профиля при регистрации пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматическое сохранение профиля при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Platform(models.Model):
    """Модель платформы/онлайн-школы"""
    name = models.CharField(max_length=100, verbose_name="Название платформы", unique=True)
    description = models.TextField(verbose_name="Описание платформы", blank=True)
    website = models.URLField(verbose_name="Сайт платформы", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """Модель курса"""
    name = models.CharField(max_length=200, verbose_name="Название курса")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='courses', verbose_name="Платформа")
    description = models.TextField(verbose_name="Описание курса")
    course_url = models.URLField(verbose_name="Ссылка на курс", blank=True, help_text="Ссылка на страницу курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.platform.name})"
    
    def average_rating(self):
        """Вычисляет среднюю оценку курса"""
        reviews = self.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

class Review(models.Model):
    """Модель отзыва"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name="Курс")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь", null=True, blank=True)
    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.author_name} на {self.course.name}"
