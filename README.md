# ToDo List Backend Project

## Описание проекта

Данный проект представляет собой полнофункциональное приложение для управления задачами (ToDo List), разработанное с использованием современных технологий Python-стека.

## Архитектура решения

### Компоненты системы:

1. **Django Backend**: Основное веб-приложение с REST API для управления задачами и категориями
2. **PostgreSQL**: База данных для хранения всех данных
3. **Redis**: Брокер сообщений для Celery
4. **Celery**: Фоновая обработка задач для отправки уведомлений
5. **Telegram Bot**: Бот для взаимодействия с пользователями через Aiogram

### Технологический стек:

- Django 4.2+
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Aiogram 3.x + Aiogram-Dialog
- Docker + Docker Compose

## Структура проекта

```
todolist_project/
├── todolist/              # Основной Django проект
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # URL маршруты
│   ├── celery.py          # Конфигурация Celery
│   └── wsgi.py            # WSGI приложение
├── todo_api/              # API приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # ViewSets для API
│   ├── serializers.py     # Сериализаторы
│   ├── urls.py            # URL маршруты API
│   ├── admin.py           # Административный интерфейс
│   ├── tasks.py           # Celery задачи
│   └── fields.py          # Кастомное поле для PK
├── telegram_bot/          # Телеграм бот
│   ├── bot.py             # Основной модуль бота
│   ├── dialogs.py         # Диалоговые окна
│   └── main.py            # Точка входа
├── docker/                # Docker конфигурации
│   ├── Dockerfile.web     # Dockerfile для веб-приложения
│   └── Dockerfile.bot    # Dockerfile для бота
├── docker-compose.yml     # Оркестрация контейнеров
├── requirements.txt       # Python зависимости
└── .env.example           # Пример переменных окружения
```

## Уникальные особенности реализации

### Кастомный Primary Key

В соответствии с требованиями задания, для основных сущностей (Task, Category) используется кастомный генератор первичных ключей, который:

- Не использует UUID
- Не использует модуль random
- Не использует стандартные функции PostgreSQL
- Не использует целочисленные инкременты

Реализация в `todo_api/fields.py` использует комбинацию timestamp и SHA256 хэша для генерации уникальных идентификаторов.

### Временная зона

Django настроена на использование часовой зоны America/Adak (UTC-10), как указано в требованиях.

## API Endpoints

### Задачи (Tasks)
- `GET /api/tasks/` - Получить список всех задач
- `POST /api/tasks/` - Создать новую задачу
- `GET /api/tasks/{id}/` - Получить конкретную задачу
- `PUT /api/tasks/{id}/` - Обновить задачу
- `DELETE /api/tasks/{id}/` - Удалить задачу
- `GET /api/tasks/my_tasks/?user_id={id}` - Получить задачи пользователя

### Категории (Categories)
- `GET /api/categories/` - Получить список категорий
- `POST /api/categories/` - Создать новую категорию
- `GET /api/categories/{id}/` - Получить конкретную категорию
- `PUT /api/categories/{id}/` - Обновить категорию
- `DELETE /api/categories/{id}/` - Удалить категорию

## Функционал Telegram бота

### Доступные команды:
- `/start` - Запуск бота и отображение главного меню
- `/help` - Справка по использованию бота

### Возможности:
1. **Просмотр задач**: Отображение всех задач пользователя с категориями и датой создания
2. **Добавление задач**: Пошаговый диалог для создания новой задачи:
   - Ввод названия
   - Ввод описания (опционально)
   - Ввод категории (опционально)
   - Ввод даты выполнения (опционально)
   - Подтверждение создания

## Уведомления

Celery настроена для отправки уведомлений за час до наступления срока выполнения задачи. Проверка задач выполняется периодически через запланированные задачи.

## Трудности и их решение

1. **Кастомный Primary Key**: Разработано специальное поле `CustomAutoField`, которое генерирует уникальные идентификаторы на основе:
   - Текущего времени в наносекундах (time.time_ns())
   - ID процесса (os.getpid())
   - ID потока (threading.current_thread().ident)
   - Атомарного счетчика
   
   Это обеспечивает глобальную уникальность без использования запрещенных модулей uuid и random.

2. **Aiogram-Dialog интеграция**: Использована последняя версия Aiogram 3.x с библиотекой aiogram-dialog для создания интерактивных диалогов с сохранением состояния. Была исправлена ошибка импорта несуществующего класса `List` из `aiogram_dialog.widgets.kbd`.

3. **Docker networking**: Настроена внутренняя сеть `todolist_network` для взаимодействия контейнеров между собой, с использованием имен сервисов как DNS-имен.

4. **Celery с PostgreSQL**: Для result backend используется Django ORM с django_celery_results для хранения результатов задач в БД. Была добавлена переменная окружения `USE_DOCKER=True` для корректной работы с PostgreSQL в контейнерах.

5. **Исправления при запуске**:
   - Добавлен отсутствующий импорт `os` в `telegram_bot/main.py`
   - Добавлены миграции перед запуском Celery beat
   - Исправлен DEFAULT_AUTO_FIELD в settings.py

## Инструкция по запуску

### Предварительные требования:
- Docker и Docker Compose установлены
- Telegram Bot Token получен у @BotFather

### Шаги по запуску:

1. **Клонируйте репозиторий и перейдите в директорию проекта:**
```bash
git clone <repository-url>
cd todolist_project
```

2. **Создайте файл .env на основе примера:**
```bash
cp .env.example .env
```

3. **Отредактируйте файл .env и добавьте ваш Telegram Bot Token:**
```bash
nano .env
# Измените TELEGRAM_BOT_TOKEN=your-telegram-bot-token на ваш реальный токен
```

4. **Запустите все сервисы:**
```bash
docker-compose up -d --build
```

5. **Проверьте статус запущенных контейнеров:**
```bash
docker-compose ps
```

6. **Для просмотра логов:**
```bash
docker-compose logs -f
```

### Доступные сервисы после запуска:

- **Django API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Telegram Bot**: Запущен и готов к работе

### Остановка проекта:
```bash
docker-compose down
```

### Очистка данных:
```bash
docker-compose down -v
docker-compose up -d
```

## Тестирование

### API тесты:
```bash
# Запустите Django shell
docker-compose exec web python manage.py shell

# Примеры запросов к API
import requests

# Получить все задачи
response = requests.get('http://localhost:8000/api/tasks/')
print(response.json())

# Создать задачу
data = {
    'user_id': 123456789,
    'title': 'Test Task',
    'description': 'Test Description',
    'category': 1
}
response = requests.post('http://localhost:8000/api/tasks/', json=data)
print(response.json())
```

### Тестирование бота:
1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Используйте кнопки для просмотра и добавления задач

## Разработка

### Добавление новых зависимостей:
```bash
# Добавьте зависимость в requirements.txt
echo "new-package>=1.0.0" >> requirements.txt

# Пересоберите контейнеры
docker-compose up -d --build
```

### Миграции базы данных:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Лицензия

MIT License