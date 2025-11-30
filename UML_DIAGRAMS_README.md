# UML Диаграммы базы данных / UML Database Diagrams

## Файлы / Files

- `uml_diagram_ru.puml` - UML диаграмма на русском языке
- `uml_diagram_en.puml` - UML diagram in English

## Как просмотреть диаграммы / How to View Diagrams

### Вариант 1: Online (Самый простой / Easiest)

1. Откройте http://www.plantuml.com/plantuml/uml/
2. Скопируйте содержимое файла `.puml`
3. Вставьте в текстовое поле
4. Нажмите "Submit" для генерации изображения

### Вариант 2: VS Code Extension

1. Установите расширение "PlantUML" в VS Code
2. Откройте файл `.puml`
3. Нажмите `Alt+D` для предварительного просмотра
4. Или используйте команду: `PlantUML: Preview Current Diagram`

### Вариант 3: Локальная установка PlantUML

#### Windows:
```bash
# Установите Java (если еще не установлена)
# Скачайте plantuml.jar с https://plantuml.com/download

# Генерация PNG
java -jar plantuml.jar uml_diagram_ru.puml
java -jar plantuml.jar uml_diagram_en.puml

# Генерация SVG
java -jar plantuml.jar -tsvg uml_diagram_ru.puml
java -jar plantuml.jar -tsvg uml_diagram_en.puml
```

#### Linux/macOS:
```bash
# Установка через package manager
sudo apt install plantuml  # Ubuntu/Debian
brew install plantuml      # macOS

# Генерация изображений
plantuml uml_diagram_ru.puml
plantuml uml_diagram_en.puml
```

### Вариант 4: Docker

```bash
# Генерация PNG
docker run --rm -v $(pwd):/data plantuml/plantuml uml_diagram_ru.puml
docker run --rm -v $(pwd):/data plantuml/plantuml uml_diagram_en.puml

# Генерация SVG
docker run --rm -v $(pwd):/data plantuml/plantuml -tsvg uml_diagram_ru.puml
docker run --rm -v $(pwd):/data plantuml/plantuml -tsvg uml_diagram_en.puml
```

## Описание диаграммы / Diagram Description

### Модели / Models

1. **User** - Встроенная модель Django для пользователей / Django built-in user model
2. **UserProfile** - Профиль пользователя с аватаром и био / User profile with avatar and bio
3. **Category** - Категории курсов / Course categories
4. **Platform** - Платформы (Coursera, Udemy и т.д.) / Platforms (Coursera, Udemy, etc.)
5. **Course** - Курсы с модерацией / Courses with moderation
6. **Review** - Отзывы с рейтингом 1-5 / Reviews with 1-5 rating

### Связи / Relationships

- **User ↔ UserProfile**: 1:1 (One-to-One)
- **User ↔ Review**: 1:N (One-to-Many)
- **User ↔ Course**: 1:N (One-to-Many, created_by)
- **Platform ↔ Course**: 1:N (One-to-Many)
- **Category ↔ Course**: M:N (Many-to-Many)
- **Course ↔ Review**: 1:N (One-to-Many)

### Обозначения / Notation

- **PK** (Primary Key) - Первичный ключ / Primary key
- **FK** (Foreign Key) - Внешний ключ / Foreign key
- **<<unique>>** - Уникальное значение / Unique constraint
- **<<nullable>>** - Может быть NULL / Can be NULL
- **[1-5]** - Диапазон значений / Value range

## Экспорт в другие форматы / Export to Other Formats

PlantUML поддерживает множество форматов:

```bash
# PNG (по умолчанию)
plantuml uml_diagram_ru.puml

# SVG (векторная графика)
plantuml -tsvg uml_diagram_ru.puml

# PDF
plantuml -tpdf uml_diagram_ru.puml

# ASCII art
plantuml -ttxt uml_diagram_ru.puml

# LaTeX
plantuml -tlatex uml_diagram_ru.puml
```

## Редактирование диаграмм / Editing Diagrams

Файлы `.puml` - это обычные текстовые файлы. Вы можете редактировать их в любом текстовом редакторе.

### Основной синтаксис PlantUML:

```plantuml
' Определение класса
class ClassName {
    PK id: Integer
    --
    field_name: Type
    --
    + method_name(): ReturnType
}

' Связи
ClassA "1" -- "0..*" ClassB : relationship_name >
ClassA "1" -- "1" ClassC : one_to_one >
ClassA "0..*" -- "0..*" ClassD : many_to_many >

' Примечания
note right of ClassName
  Текст примечания
end note
```

## Интеграция с документацией / Documentation Integration

Сгенерированные изображения можно вставить в:
- README.md
- Confluence
- Wiki
- Презентации
- Техническую документацию

Пример для Markdown:
```markdown
![UML Diagram](uml_diagram_ru.png)
```

## Полезные ссылки / Useful Links

- [PlantUML Official Site](https://plantuml.com/)
- [PlantUML Class Diagram Guide](https://plantuml.com/class-diagram)
- [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)
- [VS Code PlantUML Extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)

## Автоматическая генерация / Automatic Generation

Для автоматической генерации при изменении файлов:

```bash
# Linux/macOS
plantuml -tsvg -o ./docs *.puml

# Windows
plantuml.bat -tsvg -o docs *.puml
```

Или используйте watch mode:
```bash
plantuml -tsvg -o ./docs -watch *.puml
```

## Troubleshooting

### Ошибка: "Cannot find Java"
**Решение:** Установите Java JRE или JDK
```bash
# Windows: Скачайте с https://www.java.com/
# Linux: sudo apt install default-jre
# macOS: brew install java
```

### Ошибка: "Graphviz not found"
**Решение:** Установите Graphviz (для некоторых типов диаграмм)
```bash
# Windows: Скачайте с https://graphviz.org/download/
# Linux: sudo apt install graphviz
# macOS: brew install graphviz
```

### Кириллица отображается некорректно
**Решение:** Убедитесь, что файл сохранен в UTF-8 кодировке
