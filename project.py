import os
import time
import logging

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import emoji
import telegram
from selenium.webdriver import Chrome, ChromeOptions

from event import Event

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

RETRY_TIME = 150
ENDPOINT = 'https://plus.yandex.ru/dacha/'
DRIVER_PATH = '/Users/vlad/Desktop/chromedriver'

GENRE_EMOJI = {
    'Театр': emoji.emojize(':performing_arts:'),
    'Йога': emoji.emojize(':person_in_lotus_position_light_skin_tone:'),
    'Дети': emoji.emojize(':family_woman_boy:'),
    'Музыка': emoji.emojize(':headphone:'),
    'Кино': emoji.emojize(':popcorn:')
}


def check_tokens(tg_token, tg_channel_id):
    """
    Проверяет доступность переменных окружения.
    (которые необходимы для работы программы).
    """
    logger.info('Проверяю наличие токенов')
    if (tg_token and tg_channel_id):
        return True
    else:
        logger.critical('Необходимо проверить правильность токенов')
        return False


def get_site_answer(url, driver_path):
    """Делает запрос к сайту Яндекс Дачи."""
    logger.info('Направляю запрос к сайту')
    try:
        browser_options = ChromeOptions()
        browser_options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15')
        browser_options.add_argument('--disable-blink-features=AutomationControlled')
        # Происходит открытие браузера, но на экране пользователя этого не отображается
        # из-за добавленного аргумента headless
        browser_options.add_argument('--headless')
        browser_options.add_argument('--no-sandbox')
        browser_options.add_argument('--disable-dev-shm-usage')
        browser = Chrome(driver_path, options=browser_options)
        try:
            browser.get(url)
            response = browser.page_source
        except Exception as error:
            # Проверить status_code запроса (сравнив с HTTPStatus.OK) 
            # нет возможности, так как Селениум не предоставляет эту
            # информацию по замыслу
            # Проверить, что HTTPStatus.OK можно, сделав доп. запрос
            # через библиотеку requests (атрибут status_code)
            logger.error('На данный момент сайт недоступен, '
                         'также советуем проверить правильность URL '
                         f'Ошибка: {error}')
            raise Exception('На данный момент сайт недоступен, '
                            'также советуем проверить правильность URL '
                            f'Ошибка: {error}')
    except Exception as error:
        logger.error(f'Проблема при запуске WebDriver {error}')
        raise Exception(f'Проблема при запуске WebDriver {error}')
    finally:
        browser.close()
    return response


def parse_all_events(response):
    """Преобразовывает данные в нужный формат и парсит все мероприятия"""
    logger.info('Преобразовываю данные')
    soup = BeautifulSoup(response, 'lxml')
    events_of_dacha = soup.find_all('li', class_='dacha-events__item')
    return events_of_dacha


def parse_available_events(events_of_dacha):
    """Извлекает из всех мероприятий только доступные для регистрации."""
    logger.info('Пробую извлечь доступные мероприятия')
    available_events = []

    for event in events_of_dacha:
        try:
            event.find('button', class_='ui-button '
                                        'dacha-event-card__button '
                                        'ui-button_blue '
                                        'ui-button_size-l '
                                        'ui-button_variant-default').text
        except AttributeError:
            continue

        name_of_event = event.find('h4', class_='ui-typography '
                                                'ui-typography_size-24-normal '
                                                'ui-typography_weight-medium '
                                                'ui-typography_align-left '
                                                'dacha-event-card__title').text
        date_of_event, time_of_event = event.find(
                                        'div',
                                        class_='ui-typography '
                                               'ui-typography_size-16 '
                                               'ui-typography_weight-regular '
                                               'ui-typography_align-left '
                                               'dacha-event-card__date').text.replace('·', '—').split(',')
        # Парсинг url фото мероприятия
        # photo_code = event.find('div', class_='dacha-event-card__content')
        # url_of_photo_of_event = photo.find('style').text.split('("')[1].split(' ')[0].rstrip('")')
        genre_info_parsed = event.find('span', class_='ui-typography '
                                                      'ui-typography_size-16 '
                                                      'ui-typography_weight-regular '
                                                      'ui-typography_align-left '
                                                      'dacha-event-card__description').text
        genre_of_event = ''.join(symbol for symbol in genre_info_parsed if symbol.isalpha())
        tickets_info_parsed = event.find('div', class_='ui-typography '
                                                       'ui-typography_size-16-normal '
                                                       'ui-typography_weight-regular '
                                                       'ui-typography_align-center '
                                                       'dacha-event-card__description').text
        number_of_tickets_of_event = ''.join(symbol for symbol in
                                             tickets_info_parsed
                                             if symbol.isdigit())

        available_event = Event(name_of_event, date_of_event, time_of_event,
                                genre_of_event, number_of_tickets_of_event)

        available_events.append(available_event)

    return available_events


def search_events_differences(previous_available_events, available_events):
    """Проверяет старые и новые мероприятия с одинаковым"""
    """количеством билетов на пересечения"""
    """и выбирает только уникальные новые мероприятия"""
    logger.info('Проверяю мероприятия на уникальность')
    unique_available_events = []
    if (available_events != previous_available_events and
        available_events):
        for event in available_events:
            if not any(previous_event.name == event.name and 
                       previous_event.date == event.date for 
                       previous_event in previous_available_events):
                unique_available_events.append(event)
    if unique_available_events:
        logger.info('Появились уникальные мероприятия')
    else:
        logger.info('Новых уникальных мероприятий нет')
    return unique_available_events


def make_message(unique_available_events):
    """Формирует сообщение для отправки."""
    logger.info('Формирую сообщение')
    site_url_string = f'\n<a href="{ENDPOINT}"><i>— На сайт —</i></a>'
    events_message = ''
    for event in unique_available_events:
        text_of_event = (f'\n<b>{GENRE_EMOJI[event.genre]} '
                         f'{event.name}</b>\n'
                         f'Дата и время: {event.date} | '
                         f'{event.time}\n'
                         'Количество билетов: '
                         f'{event.available_tickets}\n')
        events_message += text_of_event
    message = events_message + site_url_string
    return message


def send_message(bot, message):
    """Отправляет сообщение в Телеграм."""
    logger.info('Направляю сообщение в Телеграм')
    try:
        bot.send_message(TELEGRAM_CHANNEL_ID, message,
                         parse_mode=telegram.ParseMode.HTML,
                         disable_web_page_preview=True)
        logger.info('Сообщение направлено в Телеграм')
    except telegram.TelegramError:
        logger.error('Сбой при отправке сообщения в Телеграм')
        raise Exception('Сбой при отправке сообщения в Телеграм')


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    available_events = []

    while True:
        try:
            if check_tokens(TELEGRAM_TOKEN, TELEGRAM_CHANNEL_ID):
                response = get_site_answer(ENDPOINT, DRIVER_PATH)
                events_of_dacha = parse_all_events(response)
                previous_available_events = available_events
                available_events = parse_available_events(events_of_dacha)
                if available_events:
                    unique_available_events = search_events_differences(previous_available_events,
                                                                        available_events)
                    if unique_available_events:
                        message = make_message(unique_available_events)
                        send_message(bot, message)
                else:
                    logger.info('Нет новых доступных мероприятий')
            else:
                raise Exception('Проверь значение токенов')
        except Exception as error:
            logger.error(f'Сбой в работе программы: {error}')
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
