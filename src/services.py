from urllib.parse import urljoin

import requests

from src.constants import BASE_URL

TODOS_URL = urljoin(BASE_URL, 'todos')


def get_todos():
    print(TODOS_URL)
    response = requests.get(TODOS_URL)
    if response.ok:
        return response
    else:
        return None


def get_uncompleted_todos():
    response = get_todos()
    if response is None:
        return []
    else:
        todos = response.json()
        return [todo for todo in todos if not todo.get('completed')]
