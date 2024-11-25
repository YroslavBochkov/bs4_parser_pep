import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, PEPS_URL
from outputs import control_output
from utils import (get_response, find_tag)


def whats_new(session=None):
    """Парсинг страницы с новинками."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    if session is None:
        session = requests_cache.CachedSession()
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all('li',
                                              attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python, desc='Парсинг релизов'):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions():
    """Парсинг страницы с последними версиями."""
    session = requests_cache.CachedSession()
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = find_tag(sidebar, 'ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session=None):
    """Скачивание документации."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    if session is None:
        session = requests_cache.CachedSession()
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_table = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(main_table, 'a',
                          {'href': re.compile(r'.+pdf-a4\.zip$')}, many=True)
    for link in tqdm(pdf_a4_tag, desc='Идет скачивание'):
        pdf_a4_link = link['href']
        archive_url = urljoin(downloads_url, pdf_a4_link)
        filename = archive_url.split('/')[-1]
        archive_path = downloads_dir / filename
        response = get_response(session, archive_url)
        if response is None:
            logging.error(f'Не удалось скачать файл: {archive_url}')
            continue
        with open(archive_path, 'wb') as file:
            file.write(response.content)
        logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep():
    """Парсинг PEP-8."""
    pep_url = PEPS_URL
    session = requests_cache.CachedSession()
    response = get_response(session, pep_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    results = [('Статус', 'Количество')]
    section = find_tag(soup, 'section', attrs={'id': 'index-by-category'})

    # Начинаем логику из search_tables_info_in_section
    sections = find_tag(section, 'section', many=True)
    counted_results = {}
    log_messages = []  # List to collect log messages

    for sub_section in sections:
        table_header = find_tag(sub_section, 'h3').text
        tables = find_tag(sub_section, 'table', many=True)

        for table in tables:
            trs = find_tag(table.tbody, 'tr', many=True)
            for tr in tqdm(trs, desc=table_header[:25]):
                tds = find_tag(tr, 'td', many=True)
                status_on_main = tds[0].text.strip()  # Trim whitespace
                if status_on_main:  # Check if not empty
                    status_on_main = status_on_main[1:]

                link = tds[2].a['href']
                pep_link = urljoin(PEPS_URL, link)
                response = get_response(session, pep_link)

                if response is None:
                    return

                pep_soup = BeautifulSoup(response.text, features='lxml')
                status_tag = find_tag(pep_soup, string='Status')
                status_value = status_tag.parent.next_sibling.next_sibling.text

                counted_results[status_value] = counted_results.get(
                    status_value, 0) + 1

                # Collect log messages instead of logging them immediately
                if status_value not in EXPECTED_STATUS.get(status_on_main, []):
                    log_messages.append(
                        f'Несовпадающие статусы: \n{pep_link} \n'
                        f'Статус в карточке: {status_value} \n'
                        f'Ожидаемые статусы: {EXPECTED_STATUS[status_on_main]}'
                    )

            # Log messages for unknown status on main
            if status_on_main not in EXPECTED_STATUS:
                log_messages.append(
                    f'Неизвестный статус на главной: {status_on_main} '
                    f'\n{pep_link} \n'
                    f'Статус в карточке: {status_value} \n'
                )

    # Log all messages at once
    if log_messages:
        logging.info('\n'.join(log_messages))

    total = sum(counted_results.values())
    counted_results['Total'] = total
    results.extend(list(counted_results.items()))
    return results


MODE_TO_FUNCTION = {
    'pep': pep,
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode]()
    if results is not None:
        control_output(results, args)


if __name__ == '__main__':
    main()
