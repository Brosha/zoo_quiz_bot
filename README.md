## Описание проекта

**Цель**: Telegram-бот для определения "тотемного животного" пользователя в игровой форме с интеграцией программы опеки животных Московского зоопарка.

**Основные функции**:
1. 🎮 Интерактивная викторина из 4+ вопросов
2. 🦁 Автоматический подбор животного на основе ответов
3. 🌟 Юмористические описания и факты о животных
4. 📊 Кнопки для участия в программе опеки
5. 💌 Система отзывов с оценкой от 1 до 5 звезд
6. 🔄 Возможность перепрохождения теста

**Технологии**:
- Python 3.10+
- Библиотека `python-telegram-bot` (v20.3)
- Встроенное логгирование
- Хранение данных в оперативной памяти (user_data)
---
### Структура:

```
zoo_quiz_bot/
├── handlers/
│   ├── __init__.py
│   ├── feedback.py    # Обработка отзывов
│   ├── quiz.py        # Логика викторины
│   ├── result.py      # Показ результатов
│   └── start.py       # Команды /start и приветствие
├── data/
│   ├── __init__.py
│   ├── animals.py     # Данные о животных
│   └── questions.py   # Вопросы викторины
├── utils/
│   ├── __init__.py
│   └── logger.py      # Настройки логгирования
├── .gitignore
├── bot.py             # Основной скрипт
├── config.py          # Конфигурация (токен, ссылки)
├── README.md          # Документация
└── requirements.txt   # Зависимости
```
---
### Пример работы бота

![Пример работы бота](zoo_quiz_bot/example.png)

---

### Как запустить

1. Клонировать репозиторий:
```bash
git clone https://github.com/Brosha/zoo_quiz_bot.git
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл `config.py` с токеном бота:
```python
BOT_TOKEN = "ВАШ_ТОКЕН"
OPECA_URL = "https://moscowzoo.ru/opeka"
SUPPORT_CONTACT = "@ваш_контакт"
```

4. Запустить бота:
```bash
python bot.py
```

---


