
## Описание
Проект задеплоен на python-anywhere, посмотреть и протестировать возможно здесь: harkort.pythonanywhere.com

Проект позволяет пользователям создавать личные страницы с записями. Пользователь может предоставлять доступ до страниц другим участникам и оставлять комментарии под чужими записями    

Целью данного проекта это изучения фреймворка Django.

## Стек технологий:
Python 3.9
Django 2.2
Django ORM

## Возможности для пользователей: 

- регистрироваться и логиниться, восстанавливать пароль по почте
- создавать, редактировать, удалять свой профиль (аватар, описание)
- создавать, редактировать, удалять и просматривать свои группы и вступать в созданные другими пользователями
- создавать, редактировать, удалять свои записи
- просматривать страницы других пользователей
- комментировать записи других авторов
- подписываться на авторов, просматривать список подписок и подписчиков
- cтавить и убирать лайки на публикации

## Возможности для администратора: 

Модерация записей осуществляется через встроенную панель администратора

## Установка проекта:
- Клонировать репозиторий GitHub:
[https://github.com/xrito/hw05_final](https://github.com/xrito/hw05_final) 

- Создайте и активируйте виртуальное окружение
```
python -m venv venv  
source activate 
```

- Установите требуемые зависимости
```
pip install -r requirements.txt
```

- Сделать миграции, создать суперпользователя и собрать статику:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

- Запустите django-сервер
```
python manage.py runserver
```
**Приложение будет доступно по адресу:** _http://127.0.0.1:8000/_

### Автор

[![Telegram](https://img.shields.io/badge/-Telegram-464646?style=flat-square&logo=Telegram)](https://t.me/harkort)
[<img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg' alt='github' height='40'>](https://github.com/xrito)  


[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![pytest](https://img.shields.io/badge/-pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)
