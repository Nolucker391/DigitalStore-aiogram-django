<img src="assets/images/skills/javaSCRP.png" alt="Demo" width="130" height="20"> <img src="assets/images/skills/HTML5.png" alt="Demo" width="130" height="20"> <img src="assets/images/skills/CSS 4.15_.png" alt="Demo" width="130" height="20"> <img src="assets/images/skills/webst.png" alt="Demo" width="130" height="20">
<hr />
<br>

[![Telegram URL](https://www.dampftbeidir.de/mediafiles/tpl/icon-telegram.png)](https://t.me/nolucker_python_bot) 
<h1> Магазин-бот

## Описание

**DigitalStore 🛍️ представляет собой современное веб-приложение 🤖, построенное на основе микросервисной архитектуры с использованием Django. Система разделена на логические компоненты, обеспечивающие эффективное взаимодействие между Telegram-ботом и базой данных.**

- Каталог товаров.
- Корзина.
- Часто задаваемые вопросы.
- Бонусный раздел.


**Макеты были созданы в Figma + Photoshop. Реализация выполненыа с использованием Django, aiogram 3.**

## Демо-версия 
[Demo-version](https://github.com/user-attachments/assets/c3761052-2f59-400b-b985-7b9795ba4782)

## Схема

<img src="schema/IMG_0299.jpeg" alt="схема">

## Инструкция по запуску

1. Скопировать файлы проекта

```commandline
git clone https://github.com/Nolucker391/DigitalStore-aiogram-django.git
```

2. Создать переменные окружения .env с параметрами:

```commandline
BOT_TOKEN = str
- для оплаты PAYMENT_TOKEN = str()
```

3. Запуск проекта

```commandline
docker-compose up     
```
## Инструменты разработки
aiogram==3.18.0<br>
dj-database-url==2.3.0<br>
Django==5.1.6<br>
openpyxl==3.1.5<br>
pillow==11.1.0<br>
pydantic==2.10.6






