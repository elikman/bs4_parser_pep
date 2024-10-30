from pathlib import Path
import re


class HTMLTag:
    """Константы для HTML тегов, используемых в парсере."""
    DIV = 'div'
    LI = 'li'
    H1 = 'h1'
    DL = 'dl'
    UL = 'ul'
    A = 'a'
    ABBR = 'abbr'
    SECTION = 'section'
    TABLE = 'table'


class RegexPatterns:
    """Регулярные выражения, используемые в парсере."""
    # Докстринг для атрибута класса должен быть в виде комментария
    # Регулярное выражение для поиска ссылки на PDF файл с размером A4
    PDF_A4_LINK = re.compile(r'.+pdf-a4\.zip$')

    # Регулярное выражение для извлечения версии и статуса Python
    PYTHON_VERSION_STATUS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'


# Базовая директория проекта
BASE_DIR = Path(__file__).parent

# Основной URL документации Python
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_DOC_PEP_URL = 'https://peps.python.org/'

# URL документации PEP
PEP_DOC_URL = 'https://peps.python.org/'

PATTERN_NUMBER_OF_PEP = r'(?P<number_of_pep>^\d+$)'

# Словарь соответствия статусов PEP
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

# Формат логирования
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

# Форматы даты и времени
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Типы вывода данных
PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'

# Путь к директории для загрузок
DOWNLOAD_DIR_PATH = 'downloads'

# Кодировка для CSV файлов
CSV_ENCODING = 'utf-8'
