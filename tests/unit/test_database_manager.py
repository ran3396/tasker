import pytest
from unittest.mock import MagicMock


def test_database_manager_execute(db_manager, mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Test'}]
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch.object(db_manager, 'get_connection', return_value=MagicMock(__enter__=MagicMock(return_value=mock_connection)))

    result = db_manager.execute("SELECT * FROM test")
    assert result == [{'id': 1, 'name': 'Test'}]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test", None)
    mock_connection.commit.assert_called_once()
