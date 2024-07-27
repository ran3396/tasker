import pytest
from unittest.mock import MagicMock


def test_cache_manager_get(cache_manager, mocker):
    mock_redis = MagicMock()
    mock_redis.get.return_value = b'test_value'
    mocker.patch.object(cache_manager, 'get_connection', return_value=MagicMock(__enter__=MagicMock(return_value=mock_redis)))

    result = cache_manager.get('test_key')
    assert result == b'test_value'
    mock_redis.get.assert_called_once_with('test_key')


def test_cache_manager_set(cache_manager, mocker):
    mock_redis = MagicMock()
    mocker.patch.object(cache_manager, 'get_connection', return_value=MagicMock(__enter__=MagicMock(return_value=mock_redis)))

    cache_manager.set('test_key', 'test_value', expire=60)
    mock_redis.setex.assert_called_once_with('test_key', 60, 'test_value')

    cache_manager.set('test_key', 'test_value')
    mock_redis.set.assert_called_once_with('test_key', 'test_value')
