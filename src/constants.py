# constants.py
from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'

PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

WHATS_NEW_TABLE = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
LATEST_VERSIONS_TABLE = [('Ссылка на документацию', 'Версия', 'Статус')]
PEP_TABLE = [('Статус', 'Количество')]

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
