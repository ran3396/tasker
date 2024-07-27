import pytest
from app.models.task import Task
import uuid


def test_task_create(db_manager):
    test_uuid = uuid.uuid4()
    task = Task.create(db_manager, str(test_uuid), 'test_task', {'param': 'value'})
    assert isinstance(uuid.UUID(task.uuid), uuid.UUID)
    assert task.name == 'test_task'
    assert task.parameters == {'param': 'value'}
    assert task.status == 'PENDING'


def test_task_get(db_manager, mocker):
    mock_execute = mocker.patch.object(db_manager, 'execute')
    mock_execute.return_value = [{
        'uuid': 'test-uuid',
        'name': 'test_task',
        'parameters': '{"param": "value"}',
        'status': 'COMPLETED',
        'output': '{"result": 42}'
    }]

    task = Task.get(db_manager, 'test-uuid')
    assert task.uuid == 'test-uuid'
    assert task.name == 'test_task'
    assert task.parameters == '{"param": "value"}'
    assert task.status == 'COMPLETED'
    assert task.output == '{"result": 42}'


def test_task_update_status(db_manager, mocker):
    mock_execute = mocker.patch.object(db_manager, 'execute')
    task = Task('test-uuid', 'test_task', {'param': 'value'}, 'PENDING')
    task.update_status(db_manager, 'COMPLETED', {'result': 42})
    assert task.status == 'COMPLETED'
    assert task.output == {'result': 42}
    mock_execute.assert_called_once()
