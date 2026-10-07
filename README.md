# Warehouse Management System (bosco-backend)

Навчальний Django-проєкт для управління складом автозапчастин.
**Практична робота № 2.5: Складський застосунок на шаблонах в Django.**

---

## Інформація про варіант та автора

- **Група:** ІТ-22
- **Варіант:** №11 — Автозапчастини
- **Модель:** `Product`
  - `name` — назва деталі;
  - `vehicle_brand` — марка автомобіля;
  - `part_number` — номер деталі (Part Number);
  - `origin_country` — країна походження;
  - `price` — ціна.

---

## Структура репозиторію

```text
bosco-backend/
├── README.md                      # Опис проєкту, варіанту та інструкції запуску
├── .gitignore                     # Ігнорування .venv/, db.sqlite3, __pycache__/, .env
├── SELF-STUDY.md                  # Звіт із самоопрацювання та результатами 3-х експериментів
└── warehouse/                     # Основний каталог Django-проєкту
    ├── manage.py
    ├── requirements.txt           # Список залежностей
    ├── config/                    # Налаштування Django-проєкту (settings.py, urls.py, wsgi.py)
    ├── templates/                 # Базові шаблони та фрагменти (base.html, partials/)
    │   ├── base.html              # Каркас сторінок (title, content, load static)
    │   └── partials/
    │       ├── menu.html          # Навігаційне меню з тегом кількості товарів
    │       └── messages.html      # Відображення flash-повідомлень (django.contrib.messages)
    └── catalog/                   # Застосунок каталогу автозапчастин
        ├── models.py              # Модель Product
        ├── views.py               # Контролери (products_list, add_product, replenish)
        ├── admin.py               # Налаштування адмін-панелі
        ├── templatetags/          # Власні DTL теги та фільтри
        │   ├── __init__.py
        │   └── catalog_extras.py  # Фільтр `uah` (ціна) та simple_tag `product_count`
        ├── static/                # Статичні файли (CSS)
        │   └── catalog/
        │       └── css/
        │           └── style.css  # Стилізація таблиць, карток, навігації та форм
        ├── templates/             # Шаблони застосунку catalog
        │   └── catalog/
        │       ├── products.html  # Таблиця деталей (extends base.html, for, empty, counter)
        │       └── add_product.html # Форма створення запчастини ({% csrf_token %})
        └── fixtures/
            └── products.json      # Початкові тестові дані
```

---

## Встановлення та запуск

1. Перейти в каталог проєкту:
   ```bash
   cd /Users/danger/Desktop/django/warehouse
   ```

2. Активувати віртуальне середовище:
   ```bash
   source .venv/bin/activate
   ```

3. Встановити залежності (за потреби):
   ```bash
   pip install -r requirements.txt
   ```

4. Застосувати міграції:
   ```bash
   python manage.py migrate
   ```

5. Завантажити початкові тестові дані автозапчастин:
   ```bash
   python manage.py loaddata products
   ```

6. Запустити сервер розробки:
   ```bash
   python manage.py runserver
   ```

---

## Основні маршрути (Endpoints)

| Маршрут | Назва | Опис |
| :--- | :--- | :--- |
| `http://127.0.0.1:8000/` | `products_list` | Каталог автозапчастин (таблиця, лічильник `forloop.counter`, фільтр `uah`) |
| `http://127.0.0.1:8000/products/` | `products` | Аліас сторінки каталогу автозапчастин |
| `http://127.0.0.1:8000/products/add/` | `add_product` | Форма додавання нової автозапчастини з CSRF-захистом та повідомленнями |
| `http://127.0.0.1:8000/replenish/5` | `replenish` | Швидке додавання 5 випадкових згенерованих деталей на склад |
| `http://127.0.0.1:8000/admin/` | `admin` | Панель адміністратора Django |

---

## Реалізовані уроки та функціонал (ПР №2.5)

- **Урок №1:** Виведення товарів через DTL-шаблон `render()`, циклічний вивід `{% for %}`, нумерація `{{ forloop.counter }}`, обробка порожнього стану `{% empty %}`, перевірка захисту від XSS через автоекранування.
- **Урок №2:** Наслідування шаблонів (`{% extends 'base.html' %}`), блоки `{% block title %}` та `{% block content %}`, винесення меню у фрагмент `templates/partials/menu.html` через `{% include %}`, генерація посилань через `{% url %}`.
- **Урок №3:** Створення власних DTL-розширень у `catalog/templatetags/catalog_extras.py`:
  - Кастомний фільтр `{{ product.price|uah }}` — форматування ціни в гривнях.
  - Кастомний `simple_tag` `{% product_count %}` — динамічний бейдж кількості деталей у навігації.
- **Урок №4:** Підключення статичних файлів через `{% load static %}` та `{% static 'catalog/css/style.css' %}`. Оформлення інтерфейсу, таблиць, кнопок та бейджів.
- **Урок №5:** Форма створення запчастини з тегом безпеки `{% csrf_token %}`, обробка POST-запиту у view, додавання повідомлень `messages.success()` та перенаправлення `redirect()`, фрагмент `partials/messages.html`.
- **Урок №6:** Створення звіту з дослідженнями `SELF-STUDY.md` (3 експерименти: XSS автоекранування, `DEBUG=False` поведінка статики, CSRF 403 Forbidden).
