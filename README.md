### Hexlet tests and linter status:
[![Actions Status](https://github.com/pavelkoA/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/pavelkoA/python-project-52/actions)
[![Actions Status](https://github.com/pavelkoA/python-project-52/actions/workflows/test.yml/badge.svg)](https://github.com/pavelkoA/python-project-83/actions/workflows/test.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/d3194180e77a5d538929/maintainability)](https://codeclimate.com/github/pavelkoA/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d3194180e77a5d538929/test_coverage)](https://codeclimate.com/github/pavelkoA/python-project-52/test_coverage)


<h1>Менеджер задач</h1>

Веб приложение для управления задачами.  
Пользователям доступно управление своими задачами и просмотр чужих задач.  
Есть возможность создавать задачи, устанавливат статусы, метки и исполнителей.


## Содержание
- [Библиотеки](#библиотеки)
- [Установка пакета](#установка-пакета)
- [Ссылка на render.com](#ссылка-render.com)


## Библиотеки
- [Python3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap5](https://getbootstrap.com/)
- [rollbar](https://rollbar.com/)


## Установка пакета

1. Вводим команду для клонирования репозитория
```sh
git clone git+https://github.com/pavelkoA/python-project-52.git
```

2. Переходим в директорию с программой
```sh
cd python-project-52
```

3. Переиеннуем файл .env.example в .env  
   В SECRET_KEY необходимо указать секретный ключ (нужен для работы Django)  
   В POST_SERVER_ITEM_ACCESS_TOKEN указываем токен от rollbar (необходим что бы ошибки отправлялись в сервис rollbar)  
   В DATABASE_URL необходимо вставить данные для подключения к базе банных:
   - USER_DB - пользователь базы данных
   - PASSWORD_DB - пароль для подключения к базе данных
   - HOST_DB - хост на котором расположена база (есди на локальном компьютере то localhost или 127.0.0.1)
   - PORT_DB - порт базы данных (по умолчанию 5432)
   - NAME_DB - имя базы данных


4. Устанавливаем необходимые зависимости и создаем таблицы в базе данных
   Для установки потребуется утилита [poetry](https://python-poetry.org/docs/)
```sh
make install
```


5. Для старта приложения можно воспользоваться командой.  
```sh
make start
```


## Ссылка на render.com

[Демонстрационная версия приложения](https://python-project-52-j3e4.onrender.com)
