# Задание 2: тестирование API Stellar Burgers

Автотесты покрывают создание и авторизацию пользователя, изменение данных
пользователя, создание заказов и получение заказов конкретного пользователя.
Для каждого эндпоинта используется отдельный тестовый класс.

## Установка зависимостей

```shell
python -m pip install -r requirements.txt
```

## Запуск тестов с сохранением результатов Allure

```shell
python -m pytest tests --alluredir=allure-results --clean-alluredir
```

## Создание и просмотр Allure-отчёта

```shell
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Тестовые пользователи получают уникальные данные и удаляются после каждого
теста, в котором они создаются.
