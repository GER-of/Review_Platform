# Руководство по миграции с SQLite на PostgreSQL

## Быстрая миграция (если у вас уже есть данные в SQLite)

### Шаг 1: Экспорт данных из SQLite
```bash
python export_data.py
```
Это создаст файл `data_backup.json` с вашими данными.

### Шаг 2: Установка PostgreSQL
См. подробную инструкцию в `POSTGRESQL_SETUP.md`

Кратко:
- Установите PostgreSQL
- Создайте базу данных `course_reviews_db`
- Запомните пароль

### Шаг 3: Настройка Django
Отредактируйте `project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'course_reviews_db',
        'USER': 'postgres',
        'PASSWORD': 'ваш_пароль',  # Ваш пароль PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Шаг 4: Установка драйвера PostgreSQL
```bash
pip install psycopg2-binary
```

### Шаг 5: Создание структуры БД
```bash
python manage.py migrate
```

### Шаг 6: Импорт данных
```bash
python import_data.py
```

### Шаг 7: Проверка
```bash
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и проверьте, что все данные на месте.

## Новая установка (без существующих данных)

Если вы начинаете с нуля:

1. Установите PostgreSQL
2. Создайте базу данных
3. Настройте `settings.py`
4. Выполните:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Откат на SQLite (если что-то пошло не так)

1. Закомментируйте PostgreSQL конфигурацию в `settings.py`
2. Раскомментируйте SQLite конфигурацию
3. Перезапустите сервер

Ваши данные в SQLite останутся нетронутыми в файле `db.sqlite3`.

## Проверка успешной миграции

После миграции проверьте:
- ✓ Все курсы отображаются
- ✓ Отзывы на месте
- ✓ Пользователи могут войти
- ✓ Аватары загружаются
- ✓ Можно добавить новый курс
- ✓ Можно оставить отзыв

## Частые проблемы

### "FATAL: password authentication failed"
**Решение:** Проверьте пароль в settings.py

### "could not connect to server"
**Решение:** Убедитесь, что PostgreSQL запущен
```bash
# Windows: Проверьте службу в services.msc
# Linux: sudo systemctl status postgresql
# macOS: brew services list
```

### "database does not exist"
**Решение:** Создайте базу данных:
```sql
psql -U postgres
CREATE DATABASE course_reviews_db;
\q
```

### Ошибки при импорте данных
**Решение:** 
1. Убедитесь, что миграции выполнены
2. Проверьте, что файл data_backup.json существует
3. Попробуйте импортировать вручную:
```bash
python manage.py loaddata data_backup.json
```

## Преимущества PostgreSQL

- ✓ Лучшая производительность
- ✓ Поддержка больших объемов данных
- ✓ Расширенные возможности индексации
- ✓ Полнотекстовый поиск
- ✓ Готовность к продакшену
- ✓ Лучшая поддержка параллельных запросов

## Бэкапы

### Создание бэкапа PostgreSQL:
```bash
pg_dump -U postgres course_reviews_db > backup.sql
```

### Восстановление:
```bash
psql -U postgres course_reviews_db < backup.sql
```

### Автоматический бэкап (рекомендуется):
Настройте регулярные бэкапы через cron (Linux) или Task Scheduler (Windows).
