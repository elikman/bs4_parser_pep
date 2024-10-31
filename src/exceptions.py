class PythonVersionsNotFound(Exception):
    """Вызывается, когда не найден список версий Python."""


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""