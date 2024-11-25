import logging

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag=None, attrs=None, string=None, many=False):
    """Перехват ошибки поиска тегов."""
    if many is False:
        searched_tag = soup.find(tag, attrs=(attrs or {}),
                                 string=(string or ''))
    else:
        searched_tag = soup.find_all(tag, attrs=(attrs or {}),
                                     string=(string or ''))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs} {string}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
