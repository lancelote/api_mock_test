# pylint: disable=invalid-name, no-member, too-few-public-methods

from unittest import skipIf
from unittest.mock import Mock, patch

from nose.tools import assert_is_none, assert_list_equal, assert_true

from src.constants import SKIP_REAL
from src.services import get_todos, get_uncompleted_todos


class TestTodos(object):

    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('src.services.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_todos_when_response_is_ok(self):
        todos = [{
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }]
        self.mock_get.return_value = Mock(ok=True)
        self.mock_get.return_value.json.return_value = todos

        response = get_todos()

        assert_list_equal(response.json(), todos)


    def test_getting_todos_when_response_is_not_ok(self):
        self.mock_get.return_value.ok = False
        response = get_todos()
        assert_is_none(response)


class TestUncompletedTodos(object):

    @classmethod
    def setup_class(cls):
        cls.mock_get_todos_patcher = patch('src.services.get_todos')
        cls.mock_get_todos = cls.mock_get_todos_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_todos_patcher.stop()

    def test_getting_uncompleted_todos_when_todos_is_not_none(self):
        todo1 = {
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }
        todo2 = {
            'userId': 1,
            'id': 2,
            'title': 'Walk the dog',
            'completed': True
        }
        self.mock_get_todos.return_value = Mock()
        self.mock_get_todos.return_value.json.return_value = [todo1, todo2]

        uncompleted_todos = get_uncompleted_todos()

        assert_true(self.mock_get_todos.called)
        assert_list_equal(uncompleted_todos, [todo1])

    def test_getting_uncompleted_todos_when_todos_is_none(self):
        self.mock_get_todos.return_value = None
        uncompleted_todos = get_uncompleted_todos()
        assert_true(self.mock_get_todos.called)
        assert_list_equal(uncompleted_todos, [])


@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
def test_integration_contract():
    actual = get_todos()
    actual_keys = actual.json().pop().keys()

    with patch('src.services.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = [{
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }]

        mocked = get_todos()
        mocked_keys = mocked.json().pop().keys()

    assert_list_equal(list(actual_keys), list(mocked_keys))
