import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import Tuple, Optional, List
from requests import Session, Response
from exceptions import PythonVersionsNotFound, ParserFindTagException

from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    EXPECTED_STATUS,
    DOWNLOAD_DIR_PATH,
    HTMLTag,
    RegexPatterns,
    MAIN_DOC_PEP_URL,
    PATTERN_NUMBER_OF_PEP
)
from configs import configure_argument_parser, configure_logging
from collections import defaultdict
from outputs import control_output
from utils import get_response, find_tag


def get_response_and_soup(
    session: Session, url: str, features: str = 'lxml'
) -> Tuple[Optional[Response], Optional[BeautifulSoup]]:
    response = get_response(session, url)
    if response is None:
        return None, None
    soup = BeautifulSoup(response.text, features)
    return response, soup


def whats_new(session: Session) -> Optional[List[Tuple[str, str, str]]]:
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response, soup = get_response_and_soup(session, whats_new_url)
    if response is None:
        return
    div_with_ul = find_tag(
        soup, HTMLTag.DIV, attrs={'class': 'toctree-wrapper'}
    )
    sections_by_python = div_with_ul.find_all(
        HTMLTag.LI, attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, HTMLTag.A)
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response, soup = get_response_and_soup(session, version_link)
        if response is None:
            continue
        h1 = find_tag(soup, HTMLTag.H1)
        dl = find_tag(soup, HTMLTag.DL)
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session: Session) -> List[Tuple[str, str, str]]:
    response, soup = get_response_and_soup(session, MAIN_DOC_URL)
    if response is None:
        return
    sidebar = find_tag(
        soup, HTMLTag.DIV, attrs={'class': 'sphinxsidebarwrapper'}
    )

    ul_tags = sidebar.find_all(HTMLTag.UL)
    for ul in ul_tags:
        if 'All versions' in ul.text:
            break
    else:
        raise PythonVersionsNotFoundException(
            'Не найден список c версиями Python'
        )


def download(session: Session) -> None:
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response, soup = get_response_and_soup(session, downloads_url)
    if response is None:
        return
    pdf_a4_tag = find_tag(
        soup, HTMLTag.A, attrs={'href': RegexPatterns.PDF_A4_LINK}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOAD_DIR_PATH
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    dict_results = defaultdict(int)
    results = [('Статус', 'Количество')]
    
    response = get_response(session, MAIN_DOC_PEP_URL)
    if response is None:
        return
        
    soup = BeautifulSoup(response.text, 'lxml')
    find_all_tags = soup.find_all('td')
    
    for tag in tqdm(find_all_tags):
        text_match = re.search(PATTERN_NUMBER_OF_PEP, tag.text)
        if not text_match:
            continue
            
        short_link = tag.find('a')['href']
        full_url = urljoin(MAIN_DOC_PEP_URL, short_link)
        status_key = tag.find_previous_sibling('td').text.strip()
        
        pep_response = get_response(session, full_url)
        if pep_response is None:
            continue
            
        pep_soup = BeautifulSoup(pep_response.text, 'lxml')
        find_tag_dt = find_tag(
            pep_soup, 'dt', attrs={'class': ['field-even', 'field-odd']}
        )
        
        while find_tag_dt and find_tag_dt.text != 'Status:':
            find_tag_dt = find_tag_dt.find_next_sibling(
                'dt', {'class': ['field-even', 'field-odd']}
            )
            
        status_in_card = find_tag_dt.find_next_sibling('dd').text
        dict_results[status_in_card] += 1
        
        expected_status = EXPECTED_STATUS[status_key[1:]]
        if status_in_card not in expected_status:
            logging.info(
                f'Несовпадающие статусы:\n'
                f'{full_url}\n'
                f'Статус в карточке: {status_in_card}\n'
                f'Ожидаемые статусы: {expected_status}\n'
            )
            
    results.extend(dict_results.items())
    results.append(('Total', sum(dict_results.values())))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main() -> None:

    configure_logging()

    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()

    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
