# Aigerin Bot — AI-воронка для психолога

Telegram-бот для автоматической записи клиентов на консультацию.

## Структура

```
aigerin-bot/
├── main.py              # Точка входа
├── requirements.txt
├── Procfile             # Для Railway
├── runtime.txt
└── bot/
    ├── config.py        # Токен и ADMIN_ID
    ├── states.py        # FSM-состояния
    ├── keyboards.py     # Inline-клавиатуры
    ├── handlers.py      # Вся логика бота
    └── scheduler.py     # Напоминания
```

---

## Деплой на Railway (шаг за шагом)

### 1. Создай GitHub репозиторий

1. Зайди на [github.com](https://github.com) → New repository
2. Назови `aigerin-bot`, Public или Private — не важно
3. Загрузи все файлы проекта

```bash
cd aigerin-bot
git init
git add .
git commit -m "init bot"
git remote add origin https://github.com/ТВОЙ_НИК/aigerin-bot.git
git push -u origin main
```

### 2. Задеплой на Railway

1. Зайди на [railway.app](https://railway.app) → **Start a New Project**
2. Выбери **Deploy from GitHub repo**
3. Авторизуй GitHub и выбери репозиторий `aigerin-bot`
4. Railway автоматически обнаружит `Procfile` и `requirements.txt`

### 3. Добавь переменные окружения

В Railway → твой проект → вкладка **Variables**, добавь:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | `8731035928:AAGhk6oDAhc1_jcTwuFeEL9F2-D0W6zMBso` |
| `ADMIN_ID` | твой Telegram chat_id (узнай у @userinfobot) |

### 4. Смени тип процесса

В Railway → Settings → убедись что запускается `worker` (не `web`).

### 5. Готово!

Бот задеплоен. Открывай своего бота в Telegram и жми /start.

---

## Как узнать свой ADMIN_ID

Напиши боту [@userinfobot](https://t.me/userinfobot) — он ответит твоим chat_id.

---

## Демо-режим напоминаний

В `bot/scheduler.py` переменная `DEMO_MODE = True`:
- Напоминание "за 24ч" придёт через **10 секунд** после записи
- Напоминание "за 2ч" придёт через **20 секунд**

Для продакшена поставь `DEMO_MODE = False` — напоминания придут в реальное время.

---

## Локальный запуск (для теста)

```bash
pip install -r requirements.txt
python3 main.py
```
