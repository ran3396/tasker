import pytest
import json
from unittest.mock import patch, Mock
import uuid


def test_run_task_integration(client):
    # Run a task
    response = client.post('/run-task', json={
        'task_name': 'sum_two_numbers',
        'task_parameters': {'a': 1, 'b': 2}
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'task_uuid' in data
    assert isinstance(uuid.UUID(data['task_uuid']), uuid.UUID)


def test_get_task_output_integration(client, task_manager, db_manager, cache_manager):
    # First, create a task
    response = client.post('/run-task', json={
        'task_name': 'sum_two_numbers',
        'task_parameters': {'a': 1, 'b': 2}
    })

    data = json.loads(response.data)

    # Then, get the task
    response = client.get(f"/get-task-output?task_uuid={data['task_uuid']}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert (data == {'task_output': {'error': None, 'status': 'PENDING', 'result': None}} or
            data == {'task_output': {'error': None, 'status': 'COMPLETED', 'result': 3}})
