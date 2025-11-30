# ER-диаграмма базы данных (UML)

## Полная UML диаграмма классов

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    Django User                                       │
│                              (встроенная модель Django)                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ PK  id: Integer                                                                     │
│     username: CharField(150) [UNIQUE]                                               │
│     email: EmailField                                                               │
│     password: CharField(128)                                                        │
│     first_name: CharField(150)                                                      │
│     last_name: CharField(150)                                                       │
│     is_staff: Boolean                                                               │
│     is_active: Boolean                                                              │
│     date_joined: DateTime                                                           │
└─────────────────────────────────────────────────────────────────────────────────────┘
                    │                                    │
                    │ 1:1                                │ 1:N
                    ▼                                    ▼
┌──────────────────────────────────┐    ┌──────────────────────────────────────────┐
│        UserProfile               │    │              Review                      │
├──────────────────────────────────┤    ├──────────────────────────────────────────┤
│ PK  id: Integer                  │    │ PK  id: Integer                          │
│ FK  user_id: Integer [UNIQUE]    │    │ FK  user_id: Integer [NULL]              │
│     bio: TextField(500)          │    │ FK  course_id: Integer                   │
│     avatar: ImageField           │    │     author_name: CharField(100)          │
│     created_at: DateTime         │    │     rating: Integer [1-5]                │
├──────────────────────────────────┤    │     text: TextField                      │
│ + __str__(): String              │    │     created_at: DateTime                 │
└──────────────────────────────────┘    ├──────────────────────────────────────────┤
                                        │ + __str__(): String                      │
                                        └──────────────────────────────────────────┘
                                                        │
                                                        │ N:1
                                                        ▼
┌──────────────────────────────────┐    ┌──────────────────────────────────────────┐
│          Category                │    │              Course                      │
├──────────────────────────────────┤    ├──────────────────────────────────────────┤
│ PK  id: Integer                  │    │ PK  id: Integer                          │
│     name: CharField(100) [UNIQUE]│◄───┤ FK  platform_id: Integer                 │
│     slug: SlugField(100) [UNIQUE]│M:N │ FK  created_by_id: Integer [NULL]        │
│     description: TextField       │    │     name: CharField(200)                 │
│     created_at: DateTime         │    │     description: TextField               │
├──────────────────────────────────┤    │     course_url: URLField                 │
│ + __str__(): String              │    │     is_approved: Boolean [DEFAULT=False] │
└──────────────────────────────────┘    │     created_at: DateTime                 │
                                        ├──────────────────────────────────────────┤
                                        │ + __str__(): String                      │
                                        │ + average_rating(): Float                │
                                        └──────────────────────────────────────────┘
                                                        │
                                                        │ N:1
                                                        ▼
                                        ┌──────────────────────────────────────────┐
                                        │            Platform                      │
                                        ├──────────────────────────────────────────┤
                                        │ PK  id: Integer                          │
                                        │     name: CharField(100) [UNIQUE]        │
                                        │     description: TextField               │
                                        │     website: URLField                    │
                                        │     created_at: DateTime                 │
                                        ├──────────────────────────────────────────┤
                                        │ + __str__(): String                      │
                                        └──────────────────────────────────────────┘
```

## Детальное описание моделей

### 1. User (Django встроенная модель)
**Назначение:** Аутентификация и авторизация пользователей

**Ключевые поля:**
- `username` - уникальное имя пользователя
- `email` - электронная почта
- `password` - хешированный пароль
- `is_staff` - доступ к админ-панели
- `date_joined` - дата регистрации

**Связи:**
- 1:1 с UserProfile
- 1:N с Review (автор отзывов)
- 1:N с Course (создатель курсов)

---

### 2. UserProfile
**Назначение:** Расширенная информация о пользователе

**Поля:**
```
id              : Integer (PK, Auto)
user_id         : Integer (FK → User, UNIQUE)
bio             : TextField (max_length=500, blank=True)
avatar          : ImageField (upload_to='avatars/', blank=True, null=True)
created_at      : DateTime (auto_now_add=True)
```

**Методы:**
- `__str__()` - возвращает "Профиль {username}"

**Особенности:**
- Автоматически создается при регистрации пользователя (signal)
- Связь OneToOne с User
- Каскадное удаление при удалении User

---

### 3. Category
**Назначение:** Категоризация курсов

**Поля:**
```
id              : Integer (PK, Auto)
name            : CharField (max_length=100, unique=True)
slug            : SlugField (max_length=100, unique=True)
description     : TextField (blank=True)
created_at      : DateTime (auto_now_add=True)
```

**Методы:**
- `__str__()` - возвращает название категории

**Примеры категорий:**
- Программирование
- Дизайн
- Маркетинг
- Бизнес
- Языки

---

### 4. Platform
**Назначение:** Платформы размещения курсов

**Поля:**
```
id              : Integer (PK, Auto)
name            : CharField (max_length=100, unique=True)
description     : TextField (blank=True)
website         : URLField (blank=True)
created_at      : DateTime (auto_now_add=True)
```

**Методы:**
- `__str__()` - возвращает название платформы

**Примеры платформ:**
- Coursera
- Udemy
- Stepik
- Skillbox
- GeekBrains

---

### 5. Course
**Назначение:** Информация о курсах

**Поля:**
```
id              : Integer (PK, Auto)
platform_id     : Integer (FK → Platform)
created_by_id   : Integer (FK → User, null=True, blank=True)
name            : CharField (max_length=200)
description     : TextField
course_url      : URLField (blank=True)
is_approved     : Boolean (default=False)
created_at      : DateTime (auto_now_add=True)
```

**Связи ManyToMany:**
- `categories` - связь с Category через промежуточную таблицу

**Методы:**
- `__str__()` - возвращает "{статус} {название} ({платформа})"
- `average_rating()` - вычисляет среднюю оценку из всех отзывов

**Бизнес-логика:**
- Курсы требуют одобрения администратора (`is_approved`)
- Только одобренные курсы видны на сайте
- Пользователи могут предлагать курсы

---

### 6. Review
**Назначение:** Отзывы пользователей о курсах

**Поля:**
```
id              : Integer (PK, Auto)
course_id       : Integer (FK → Course)
user_id         : Integer (FK → User, null=True, blank=True)
author_name     : CharField (max_length=100)
rating          : Integer (validators: 1-5)
text            : TextField
created_at      : DateTime (auto_now_add=True)
```

**Методы:**
- `__str__()` - возвращает "Отзыв от {автор} на {курс}"

**Валидация:**
- `rating` должен быть от 1 до 5 (MinValueValidator, MaxValueValidator)

---

## Связи между моделями (Cardinality)

```
User ──────1:1────── UserProfile
  │
  ├────1:N────── Review
  │
  └────1:N────── Course (created_by)

Platform ──────1:N────── Course

Category ──────M:N────── Course

Course ──────1:N────── Review
```

### Детализация связей:

| От | Связь | К | Тип | ON DELETE | related_name |
|---|---|---|---|---|---|
| User | 1:1 | UserProfile | OneToOne | CASCADE | profile |
| User | 1:N | Review | ForeignKey | CASCADE | reviews |
| User | 1:N | Course | ForeignKey | SET_NULL | created_courses |
| Platform | 1:N | Course | ForeignKey | CASCADE | courses |
| Category | M:N | Course | ManyToMany | - | courses |
| Course | 1:N | Review | ForeignKey | CASCADE | reviews |

---

## Индексы и ограничения

### Primary Keys (автоматические):
- Все таблицы имеют `id` как PK с автоинкрементом

### Foreign Keys (автоматические индексы):
- `UserProfile.user_id`
- `Review.course_id`
- `Review.user_id`
- `Course.platform_id`
- `Course.created_by_id`

### Unique Constraints:
- `User.username`
- `Platform.name`
- `Category.name`
- `Category.slug`
- `UserProfile.user_id`

### Validators:
- `Review.rating`: MinValueValidator(1), MaxValueValidator(5)

---

## Сортировка по умолчанию (Meta.ordering)

| Модель | Сортировка | Описание |
|---|---|---|
| UserProfile | - | Без сортировки |
| Category | `['name']` | По алфавиту |
| Platform | `['name']` | По алфавиту |
| Course | `['-created_at']` | Новые первыми |
| Review | `['-created_at']` | Новые первыми |

---

## Бизнес-правила

1. **Регистрация пользователя:**
   - Автоматически создается UserProfile (через signal)
   - Пользователь может войти и оставлять отзывы

2. **Добавление курса:**
   - Только авторизованные пользователи могут добавлять курсы
   - Курсы требуют одобрения администратора
   - Курс может иметь несколько категорий

3. **Отзывы:**
   - Только авторизованные пользователи могут оставлять отзывы
   - Оценка от 1 до 5 звезд
   - Отзыв привязан к пользователю и курсу

4. **Рейтинг курса:**
   - Вычисляется динамически как среднее всех оценок
   - Курсы с рейтингом > 4.5 попадают в "Рекомендуемые"

5. **Модерация:**
   - Администраторы одобряют/отклоняют курсы
   - Неодобренные курсы не видны обычным пользователям

---

## Диаграмма потоков данных

```
┌──────────────┐
│ Пользователь │
└──────┬───────┘
       │
       ├─── Регистрация ──→ User + UserProfile
       │
       ├─── Добавление курса ──→ Course (is_approved=False)
       │                              │
       │                              ↓
       │                         Администратор
       │                              │
       │                              ↓
       │                         Одобрение
       │                              │
       │                              ↓
       │                         Course (is_approved=True)
       │                              │
       │                              ↓
       └─── Оставление отзыва ──→ Review
                                      │
                                      ↓
                              Обновление рейтинга
```

---

## База данных: PostgreSQL

**Преимущества для данной схемы:**
- Эффективная работа с ForeignKey
- Поддержка сложных запросов с JOIN
- Транзакции для целостности данных
- Полнотекстовый поиск (для будущего расширения)
- Масштабируемость

**Рекомендуемые индексы для оптимизации:**
```sql
CREATE INDEX idx_course_approved ON game_course(is_approved);
CREATE INDEX idx_review_rating ON game_review(rating);
CREATE INDEX idx_course_created_at ON game_course(created_at DESC);
```
