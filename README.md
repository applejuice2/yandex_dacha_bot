# Yandex Dacha Bot

![img](https://img.shields.io/badge/license-MIT-brightgreen)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=FFFFFF&color=00B2FF)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/-Selenium-464646?style=flat&logo=Selenium&logoColor=FFFFFF&color=00B2FF)](https://www.selenium.dev)
[![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-464646?style=flat&logo=BeautifulSoup&logoColor=FFFFFF&color=00B2FF)](https://www.selenium.dev)
[![YandexCloud](https://img.shields.io/badge/-Yandex%20Cloud-464646?style=flat&logo=data:image/png;base64,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&logoColor=FFFFFF&color=00B2FF)](http://cloud.yandex.ru) 
  
### Общая информация
В середине августа моя знакомая попросила создать бота, оповещающего о новых билетах на ___«Плюс Дачу»___, которая работает с июня по сентябрь, так как  билеты всё время были в дефиците (из-за того, что они бесплатные), а сходить на мероприятия (показы фильмов, концерты известных музыкантов - _Сюзанна, Группа Звери_) хотелось. Это поспособствовало появлению **Yandex Dacha Bot**. Изначально планировал обойтись библиотекой requests, с которой бот успешно запускался на компьютере, но при деплое на [Yandex Cloud](https://cloud.yandex.ru) появлялась капча, поэтому ознакомился и использовал __Selenium__, который эмулирует запуск браузера на виртуальном сервере и помогает избежать капчи. Также в процессе работы освоил библиотеку __Beautiful Soup__.

Ознакомиться с работой бота - [https://t.me/dacha_tickets](https://t.me/dacha_tickets)

### Принцип работы:

- Раз в 150 секунд бот заходит на сайт [https://plus.yandex.ru/dacha](https://plus.yandex.ru/dacha)
- Парсит информацию
- При появлении новых бесплатных билетов формирует сообщение и отправляет его в Телеграм канал
- При этом происходит логгирование всех этапов


### Требования

- Python 3.8+
- Работает на macOS, Windows, Linux


### Запуск бота:

1. Сделайте форк репозитория и клонируйте его.

2. В клонированном репозитории создайте файл .env и заполните переменные окружения

***TELEGRAM_TO*** - id телеграм-аккаунта, которому будут приходить сообщения с результатом workflow. Узнать свой ID можно у бота *@userinfobot*.

***TELEGRAM_TOKEN*** - токен вашего бота. Получить этот токен можно у бота *@BotFather*.

3. Установите и активируйте виртуальное окружение:
 ```sh
 python -m venv venv
 source venv/bin/activate 
 ```
4. Установите зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
5. Установите Google Chrome на вашу локальную машину
6. Установите chromedriver (для работы с Selenium'ом, подходящий под версию вашего Google Chrome - [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
7. В файле project.py в переменной DRIVER_PATH установите путь до chromedriver


## Автор проекта:
- [Влад Иванов](https://github.com/applejuice2/)
