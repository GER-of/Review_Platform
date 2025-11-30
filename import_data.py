"""
Скрипт для импорта данных в PostgreSQL после миграции
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command

print("Импорт данных в PostgreSQL...")
print("=" * 50)

try:
    call_command('loaddata', 'data_backup.json')
    print("✓ Данные успешно импортированы")
    print("\nПроверьте данные:")
    print("- Откройте http://127.0.0.1:8000/admin/")
    print("- Проверьте курсы, отзывы и пользователей")
except Exception as e:
    print(f"✗ Ошибка при импорте: {e}")
    print("\nВозможные причины:")
    print("- Файл data_backup.json не найден")
    print("- Миграции не выполнены (python manage.py migrate)")
    print("- Проблемы с подключением к PostgreSQL")
