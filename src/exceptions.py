class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class MismatchedStatusException(Exception):
    """
    Вызывается, когда статус на страцице PEP и статус
    на главной странице отличаются.
    """
