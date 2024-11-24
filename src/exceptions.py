class ParserFindTagException(Exception):
    """
    Вызывается, когда тег не найден в документации Python.
    """
    pass


class MismatchedStatusException(Exception):
    """
    Вызывается, когда статус PEP не соответствует ожидаемому.
    """
