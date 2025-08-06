# Telegram Contest Bot

![Build](https://github.com/gutsy51/foodgram/actions/workflows/main.yml/badge.svg)

![aiogram](https://img.shields.io/badge/Aiogram-009cfb?logo=Python&logoColor=white)
![gspread](https://img.shields.io/badge/gspread-34A853?logo=google-sheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GH Actions](https://img.shields.io/badge/GitHub_Actions-gray?logo=github-actions&logoColor=2088FF)

## 📃 Описание

Telegram чат-бот для сбора заявок на участие в конкурсе 
[студий deza и nomo](https://t.me/addlist/dC8VZgOHixxhOTcy) на создание нового архетипа. 
Собирает заявки и сохраняет их в Google-таблицу.

## 🚀 Запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/gutsy51/fl-tg-contest-bot.git
cd fl-tg-contest-bot
```

### 2. Подготовьте переменные окружения
Создайте файл `.env` и заполните его по примеру `.env.example`.

### 3. Настройте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Запустите проект в фоновом режиме
```bash
nohup python3 bot.py & 
```

> Автор: Валерий Полуянов, GitHub: [gutsy51](https://github.com/gutsy51), Telegram: [@gutsy51](https://t.me/gutsy51)
