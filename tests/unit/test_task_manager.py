import pytest
from unittest.mock import MagicMock


def test_task_manager_create_task(task_manager, mocker):
    mock_task = MagicMock(uuid='test-uuid')
    mocker.patch('app.models.task.Task.create', return_value=mock_task)
    mock_celery = MagicMock()
    mocker.patch.object(task_manager, 'celery', mock_celery)

    result = task_manager.create_task('sum_two_numbers', {'a': 1, 'b': 2})
    assert result == 'test-uuid'
    mock_celery.send_task.assert_called_once_with('app.tasks.task_functions.sum_two_numbers', args=[1, 2])


def test_task_manager_get_task_output(task_manager, mocker):
    mocker.patch.object(task_manager.cache_manager, 'get', return_value=None)
    mock_task = MagicMock(status='COMPLETED', output=3)
    mocker.patch('app.models.task.Task.get', return_value=mock_task)

    result = task_manager.get_task_output('test-uuid')
    assert result == {'status': 'COMPLETED', 'result': 3, 'error': None}
