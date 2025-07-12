
---

# API_PETITION

Основной API: сервис для приема пользовательских жалоб, анализа их категории и тональности, а также обновления статуса обращений.

---

## Содержание

- [Структура проекта](#структура-проекта)
- [Установка](#установка)
- [Запуск](#запуск)
- [Настройка переменных окружения](#настройка-переменных-окружения)
- [Пример .env файла](#пример-env-файла)
- [Примеры запросов](#примеры-запросов)
- [API для симуляции сервисов](#api-для-симуляции-сервисов)
- [Контейнеризация (Docker)](#контейнеризация-docker)
---

## Структура проекта

```
API_PETITION/
├── API/
│   ├── app/
│   │   ├── database.py
│   │   ├── sentiment.py
│   │   └── categorize.py
│   ├── sql/
│   │   ├── config.env
│   │   └── database.sqlite
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py         # Точка входа основного API
├── test_mode_api/
│   ├── run.py         # Фейк-симулятор OpenAI и APILayer для теста
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <URL-РЕПОЗИТОРИЯ>
   cd API_PETITION
   ```

2. **Перейдите в папку API, создайте и активируйте виртуальное окружение:**
   ```bash
   cd API
   python -m venv .venv
   source .venv/bin/activate  # или .venv\Scripts\activate на Windows
   pip install -r requirements.txt
   ```
   Аналогично для необходимости запуска test_mode_api.

---

## Запуск

### Без Docker

1. **Убедитесь, что подготовлен файл `config.env` с нужными переменными:**
   ```bash
   cp sql/config.env.example sql/config.env
   # или вручную создайте файл и заполните значениями
   ```

2. **Выполните:**
   ```bash
   uvicorn run:app --reload
   # или
   python run.py
   ```
   
   API будет доступен на `http://127.0.0.1:8000` (по умолчанию).

### С помощью Docker Compose

1. **Запустите оба сервиса:**
   ```bash
   docker-compose up --build
   ```
   Это запустит основной сервис, тестовые симуляторы и n8n.

---

## Настройка переменных окружения

Для корректной работы API необходимы ключи для внешних сервисов (OpenAI, APILayer). Межсервисная интеграция для тестирования включается переменной `Test_Mode=True`.

**Переменные описаны в файле API/sql/config.env:**
- `OPENAI_API_KEY` — API-ключ OpenAI (GPT-3.5-Turbo)
- `API_LAYER_KEY` — ключ для сервиса анализа сентимента
- `Test_Mode` — булевый флаг (True/False), включает тестовый режим (для отладки без внешних сервисов)

---

Токен бота - 7963717296:AAGxvS01fWCQRUZoqFOVT1KZMVTck9SwwS8

---

## Пример .env файла

```env
API_LAYER_KEY=fvYs9OIPg8VQi9IMGtETgCeWvlIL9PqB
OPENAI_API_KEY=...
Test_Mode=True
```

*Пример настоящих ключей не выкладывайте в открытый репозиторий!*

---

## Примеры запросов

### Добавить жалобу

```bash
curl -X POST http://localhost:8000/complaints \
  -H "Content-Type: application/json" \
  -d '{"text": "У меня не проходит оплата"}'
```

### Получить все жалобы

```bash
curl http://localhost:8000/complaints
```

### Закрыть жалобу

```bash
curl -X POST http://localhost:8000/close \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### Обновить статус жалобы

```bash
curl -X PATCH http://localhost:8000/complaints/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

---

## API для симуляции сервисов (test_mode_api)

Для тестирования без реальных ключей используются поддельные endpoints, которые возвращают случайные значения категорий и сентимента:

- `/category` — случайная категория (оплата/техническая/другое)
- `/sentiment` — случайное настроение (позитивная/нейтральная/негативная)

Пример запроса:

```bash
curl http://localhost:7000/category
curl http://localhost:7000/sentiment
```

---

## Контейнеризация (Docker)

Проект полностью готов для запуска в контейнерах.  
В корне размещен файл `docker-compose.yml` — запуск производится командой:

```bash
docker-compose up --build
```

---

## Дополнительно

- Не забудьте положить свой ключ OpenAI и APILayer в файл `API/sql/config.env`!
- Для теста без ключей и внешних сервисов (только для разработки) выставьте `Test_Mode=True`.

---

### Обратная связь и вопросы

Если есть вопросы по коду, настройке фабрики, API — пишите в issues или мне напрямую.

---

