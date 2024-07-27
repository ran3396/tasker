import pytest
from app import create_app
from app.core.database_manager import DatabaseManager
from app.core.cache_manager import CacheManager
from app.core.task_manager import TaskManager


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_manager(app):
    return DatabaseManager(app.config)


@pytest.fixture
def cache_manager(app):
    return CacheManager(app.config)


@pytest.fixture
def task_manager(app, db_manager, cache_manager):
    return TaskManager(app.config, db_manager, cache_manager)
