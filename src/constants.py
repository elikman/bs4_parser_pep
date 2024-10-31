from pathlib import Path
import re


class HTMLTag:
    """Константы для HTML тегов, используемых в парсере."""

    DIV = 'div'
    """HTML тег div."""

    LI = 'li'
    """HTML тег li."""

    H1 = 'h1'
    """HTML тег h1."""

    DL = 'dl'
    """HTML тег dl."""

    UL = 'ul'
    """HTML тег ul."""

    A = 'a'
    """HTML тег a."""

    ABBR = 'abbr'
    """HTML тег abbr."""

    SECTION = 'section'
    """HTML тег section."""

    TABLE = 'table'
    """HTML тег table."""


class RegexPatterns:
    """Регулярные выражения, используемые в парсере."""

    PDF_A4_LINK = re.compile(r'.+pdf-a4\.zip$')
    """Регулярное выражение для поиска ссылки на PDF файл с размером A4."""

    PYTHON_VERSION_STATUS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    """Регулярное выражение для извлечения версии и статуса Python."""


BASE_DIR = Path(__file__).parent
"""Базовая директория проекта."""

MAIN_DOC_URL = 'https://docs.python.org/3/'
"""Основной URL документации Python."""

MAIN_DOC_PEP_URL = 'https://peps.python.org/'
"""URL документации PEP."""

PEP_DOC_URL = 'https://peps.python.org/'
"""URL документации PEP."""

PATTERN_NUMBER_OF_PEP = r'(?P<number_of_pep>^\d+$)'
"""Регулярное выражение для извлечения номера PEP."""

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
"""Словарь соответствия статусов PEP."""

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
"""Формат логирования."""

DT_FORMAT = '%d.%m.%Y %H:%M:%S'
"""Формат даты и времени."""

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
"""Формат даты и времени для имен файлов."""

PRETTY_OUTPUT = 'pretty'
"""Тип вывода данных в консоль."""

FILE_OUTPUT = 'file'
"""Тип вывода данных в файл."""

DOWNLOAD_DIR_PATH = 'downloads'
"""Путь к директории для загрузок."""

CSV_ENCODING = 'utf-8'
"""Кодировка для CSV файлов."""
