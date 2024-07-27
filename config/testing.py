from .base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Use in-memory Redis for testing
    REDIS_URL = 'memory://'
