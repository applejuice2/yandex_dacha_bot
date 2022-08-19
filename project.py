import os
import time
import logging
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import emoji
import telegram

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

RETRY_TIME = 60
ENDPOINT = 'https://plus.yandex.ru/dacha/'

GENRE_EMOJI = {
    'Театр': emoji.emojize(':performing_arts:'),
    'Йога': emoji.emojize(':person_in_lotus_position_light_skin_tone:'),
    'Дети': emoji.emojize(':family_woman_boy:'),
    'Музыка': emoji.emojize(':headphone:'),
    'Кино': emoji.emojize(':popcorn:')
}


def check_tokens():
    """
    Проверяет доступность переменных окружения.
    (которые необходимы для работы программы).
    """
    logger.info('Проверяю наличие токенов')
    if (TELEGRAM_TOKEN and TELEGRAM_CHANNEL_ID):
        return True
    else:
        logger.critical('Необходимо проверить правильность токенов')
        return False


def get_site_answer():
    """Делает запрос к сайту Яндекс Дачи."""
    logger.info('Направляю запрос к сайту')
    try:
        response = requests.get(ENDPOINT)
        if response.status_code != HTTPStatus.OK:
            logger.error('На данный момент сайт недоступен')
            raise Exception('На данный момент сайт недоступен')
    except Exception:
        logger.error('Неверный URL')
        raise Exception('Неверный URL')

    return response


def parse_all_events(response):
    """Преобразовывает данные в нужный формат и парсит все мероприятия"""
    logger.info('Преобразовываю данные')
    soup = BeautifulSoup(response.text, 'lxml')
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

        info_about_event = (f'\n<b>{GENRE_EMOJI[genre_of_event]} '
                            f'{name_of_event}</b>\n'
                            f'Дата и время: {date_of_event} | '
                            f'{time_of_event}\n'
                            'Количество билетов: '
                            f'{number_of_tickets_of_event}\n')

        available_events.append(info_about_event)

    return available_events


def search_events_differences(previous_available_events, available_events):
    """Проверяет старые и новые мероприятия с одинаковым"""
    """количеством билетов на пересечения"""
    """и выбирает только уникальные новые мероприятия"""
    logger.info('Проверяю мероприятия на уникальность')
    if (available_events != previous_available_events and
            (set(available_events) & set(previous_available_events))):
        logger.info('Появились уникальные мероприятия')
        available_events = [event for event in available_events
                            if event not in previous_available_events]
    else:
        logger.info('Новых уникальных мероприятий нет')
    return available_events


def make_message(available_events):
    """Формирует сообщение для отправки."""
    logger.info('Формирую сообщение')
    if available_events:
        site_url_string = f'\n<a href="{ENDPOINT}"><i>— На сайт —</i></a>'
        available_events = ''.join(available_events)
        message = available_events + site_url_string
    else:
        message = available_events
    return message


def send_message(bot, message):
    """Отправляет сообщение в Telegram."""
    logger.info('Направляю сообщение в Telegram')
    try:
        bot.send_message(TELEGRAM_CHANNEL_ID, message,
                         parse_mode=telegram.ParseMode.HTML,
                         disable_web_page_preview=True)
        logger.info('Сообщение направлено в Телеграм')
    except telegram.TelegramError:
        logger.error('Сбой при отправке сообщения в Telegram')
        raise Exception('сбой при отправке сообщения в Telegram')


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    available_events = []

    while True:
        try:
            if check_tokens():
                response = get_site_answer()
                events_of_dacha = parse_all_events(response)
                previous_available_events = available_events
                available_events = parse_available_events(events_of_dacha)
                if available_events:
                    available_events = search_events_differences(previous_available_events,
                                                                available_events)
                    if available_events:
                        message = make_message(available_events)
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
