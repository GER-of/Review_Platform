from django import template

register = template.Library()

@register.filter
def pluralize_reviews(count):
    """
    Склонение слова 'отзыв' в зависимости от числа
    1 отзыв
    2, 3, 4 отзыва
    5, 6, 7, 8, 9, 0 отзывов
    """
    count = int(count)
    
    # Для чисел от 11 до 19 всегда "отзывов"
    if 11 <= count % 100 <= 19:
        return f"{count} отзывов"
    
    # Для остальных смотрим на последнюю цифру
    last_digit = count % 10
    
    if last_digit == 1:
        return f"{count} отзыв"
    elif 2 <= last_digit <= 4:
        return f"{count} отзыва"
    else:
        return f"{count} отзывов"
