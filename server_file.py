import logging
import requests
from http import HTTPStatus
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import emoji
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

GENRE_EMOJI = {
    'Театр': emoji.emojize(':performing_arts:'),
    'Йога': emoji.emojize(':person_in_lotus_position_light_skin_tone:'),
    'Дети': emoji.emojize(':family_woman_boy:'),
    'Музыка': emoji.emojize(':headphone:'),
    'Кино': emoji.emojize(':popcorn:')
}

ENDPOINT = 'https://plus.yandex.ru/dacha/'
# ENDPOINT = 'https://httpbin.org/get'
# ENDPOINT = 'http://habr.ru'
# proxy = {'http': '127.0.0.1:8080'}
# requests.get(ENDPOINT, proxies=proxy)
def get_site_answer():
    """Делает запрос к сайту Яндекс Дачи."""
    logger.info('Направляю запрос к сайту')
    # try:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"}
    cookie = {'_yasc': 'vMMKwXyCOnGJE1EuMT3wADKb/id3fCFZWLQ4FcQcf2fV4w'}
    proxy = {'https': '95.154.64.101:8080'}
    # response = requests.get(ENDPOINT, proxies=proxy, verify=False, headers=headers)
    response = requests.get(ENDPOINT, proxies=proxy, verify=False, headers=headers)
    response.encoding = 'utf8'
    if response.status_code != HTTPStatus.OK:
        logger.error('На данный момент сайт недоступен')
        raise Exception('На данный момент сайт недоступен')
    # except Exception:
    #     logger.error('Неверный URL')
    #     raise Exception('Неверный URL')

    print(response.text)
    print(response.cookies)
    # print(response.content)
    return response


def parse_all_events(response):
    """Преобразовывает данные в нужный формат и парсит все мероприятия"""
    logger.info('Преобразовываю данные')
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
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

response = get_site_answer()
# # events_of_dacha = parse_all_events(response)
# # available_events = parse_available_events(events_of_dacha)
# # print(available_events)