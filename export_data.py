"""
Скрипт для экспорта данных из SQLite перед переходом на PostgreSQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command

print("Экспорт данных из SQLite...")
print("=" * 50)

try:
    # Экспортируем все данные кроме системных таблиц
    call_command(
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '--indent', '4',
        '--output', 'data_backup.json'
    )
    print("✓ Данные успешно экспортированы в data_backup.json")
    print("\nТеперь вы можете:")
    print("1. Настроить PostgreSQL в settings.py")
    print("2. Выполнить: python manage.py migrate")
    print("3. Выполнить: python manage.py loaddata data_backup.json")
except Exception as e:
    print(f"✗ Ошибка при экспорте: {e}")
