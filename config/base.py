import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    
    # Database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'taskdb')
    DB_USER = os.environ.get('DB_USER', 'taskuser')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    
    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    
    # Celery
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # ChatGPT
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-api-key')
