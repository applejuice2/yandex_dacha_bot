# Yandex Dacha Bot

![img](https://img.shields.io/badge/license-MIT-brightgreen)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=FFFFFF&color=00B2FF)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/-Selenium-464646?style=flat&logo=Selenium&logoColor=FFFFFF&color=00B2FF)](https://www.selenium.dev)
[![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-464646?style=flat&logo=BeautifulSoup&logoColor=FFFFFF&color=00B2FF)](https://www.selenium.dev)
[![YandexCloud](https://img.shields.io/badge/-Yandex%20Cloud-464646?style=flat&logoColor=FFFFFF&color=00B2FF)](http://cloud.yandex.ru) 
  
### Общая информация
В середине августа моя знакомая попросила создать бота, который бы оповещал о новых билетах на ___«Плюс Дачу»___, которая работает с июня по сентябрь, так как  билеты всё время были в дефиците (из-за того, что они бесплатные), а сходить на мероприятия (показы фильмов, концерты известных музыкантов - _Сюзанна, Группа Звери_) хотелось. Так и появился **Yandex Dacha Bot**. Изначально планировал обойтись библиотекой requests, с которой бот успешно запускался на компьютере, но при деплое на [Yandex Cloud](https://cloud.yandex.ru) появлялась капча, поэтому ознакомился и использовал __Selenium__, который эмулирует запуск браузера на виртуальном сервере и помогает изюежать капчи. Также в процессе работы освоил библиотеку __Beautiful Soup__.

Ознакомиться с работой бота - [https://t.me/dacha_tickets](https://t.me/dacha_tickets)

### Принцип работы:

- Раз в 150 секунд бот заходит на сайт [https://plus.yandex.ru/dacha](https://plus.yandex.ru/dacha)
- Парсит информацию
- При появлении новых бесплатных билетов формирует сообщение и отправляет его в Телеграм канал
- При этом происходит логгирование всех этапов


### Требования

- Python 3.7+
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
