# Настройка PostgreSQL для проекта

## Установка PostgreSQL

### Windows:
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Запустите установщик
3. Запомните пароль для пользователя `postgres`
4. По умолчанию порт: `5432`

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS:
```bash
brew install postgresql
brew services start postgresql
```

## Создание базы данных

### Способ 1: Через psql (командная строка)

1. Войдите в PostgreSQL:
```bash
psql -U postgres
```

2. Создайте базу данных:
```sql
CREATE DATABASE course_reviews_db;
```

3. Создайте пользователя (опционально):
```sql
CREATE USER course_user WITH PASSWORD 'your_password';
ALTER ROLE course_user SET client_encoding TO 'utf8';
ALTER ROLE course_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE course_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE course_reviews_db TO course_user;
```

4. Выйдите:
```sql
\q
```

### Способ 2: Через pgAdmin (GUI)

1. Откройте pgAdmin
2. Подключитесь к серверу PostgreSQL
3. Правый клик на "Databases" → "Create" → "Database"
4. Введите имя: `course_reviews_db`
5. Нажмите "Save"

## Настройка проекта Django

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте `.env.example` в `.env`:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS
```

3. Отредактируйте `.env` и укажите ваши настройки:
```
DB_NAME=course_reviews_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

4. Или отредактируйте `project/settings.py` напрямую:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'course_reviews_db',
        'USER': 'postgres',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Миграция данных

### Если начинаете с нуля:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Если переносите данные из SQLite:

1. Экспортируйте данные из SQLite:
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data.json
```

2. Переключитесь на PostgreSQL в settings.py

3. Создайте структуру БД:
```bash
python manage.py migrate
```

4. Импортируйте данные:
```bash
python manage.py loaddata data.json
```

## Проверка подключения

Запустите сервер:
```bash
python manage.py runserver
```

Если все настроено правильно, сервер запустится без ошибок.

## Полезные команды PostgreSQL

### Просмотр всех баз данных:
```sql
\l
```

### Подключение к базе данных:
```sql
\c course_reviews_db
```

### Просмотр таблиц:
```sql
\dt
```

### Просмотр структуры таблицы:
```sql
\d table_name
```

### Удаление базы данных (осторожно!):
```sql
DROP DATABASE course_reviews_db;
```

## Решение проблем

### Ошибка: "FATAL: password authentication failed"
- Проверьте пароль в settings.py
- Убедитесь, что пользователь существует

### Ошибка: "could not connect to server"
- Убедитесь, что PostgreSQL запущен
- Проверьте HOST и PORT в настройках

### Ошибка: "database does not exist"
- Создайте базу данных через psql или pgAdmin

### Windows: PostgreSQL не запускается
- Откройте "Службы" (services.msc)
- Найдите "postgresql-x64-XX"
- Запустите службу

## Бэкап и восстановление

### Создание бэкапа:
```bash
pg_dump -U postgres course_reviews_db > backup.sql
```

### Восстановление из бэкапа:
```bash
psql -U postgres course_reviews_db < backup.sql
```
