from app import create_app
from celery import Celery
from app.tasks import task_functions
from app.tasks import callbacks

app = create_app('development')
celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'])

celery.conf.update(app.config)

# This line ensures that task modules are loaded
celery.autodiscover_tasks(['app.tasks'], force=True)

if __name__ == '__main__':
    celery.start()
