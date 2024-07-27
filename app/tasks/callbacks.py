import json
from typing import Any
from celery.signals import task_success, task_failure
from dotenv import load_dotenv

from app.models.task import Task
from app.core.database_manager import DatabaseManager
from app.core.cache_manager import CacheManager

load_dotenv()


class TaskCallbackManager:
    def __init__(self, db_manager: DatabaseManager, cache_manager: CacheManager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def initialize_callbacks(self):
        task_success.connect(self.task_success_handler)
        task_failure.connect(self.task_failure_handler)

    def task_success_handler(self, sender=None, result=None, **kwargs):
        # Update the task status in the database and cache in case of success
        print(f"Task {sender.request.id} completed successfully")
        task_id = sender.request.id
        task = Task.get(self.db_manager, task_id)
        if task:
            task.update_status(self.db_manager, 'COMPLETED', result)
            self._update_cache(task_id, 'SUCCESS', result)

    def task_failure_handler(self, sender=None, exception=None, **kwargs):
        # Update the task status in the database and cache in case of failure
        print(f"Task {sender.request.id} failed: {str(exception)}")
        task_id = sender.request.id
        task = Task.get(self.db_manager, task_id)
        if task:
            error = str(exception)
            task.update_status(self.db_manager, 'FAILED', {'error': error})
            self._update_cache(task_id, 'FAILURE', error)

    def _update_cache(self, task_id: str, status: str, result: Any):
        # Update the task status in the cache
        cache_key = f'celery-task-meta-{task_id}'
        cache_value = self.cache_manager.get(cache_key)

        if cache_value:
            try:
                task_meta = json.loads(cache_value)
            except json.JSONDecodeError:
                task_meta = {}
        else:
            task_meta = {}

        task_meta.update({
            'status': status,
            'result': result,
            'task_id': task_id,
        })

        self.cache_manager.set(cache_key, json.dumps(task_meta), expire=3600)  # Cache for 1 hour


# Create a singleton instance
callback_manager = None


def initialize_callback_manager(db_manager: DatabaseManager, cache_manager: CacheManager):
    global callback_manager
    callback_manager = TaskCallbackManager(db_manager, cache_manager)
    callback_manager.initialize_callbacks()


# These functions are kept for compatibility with Celery's signal connection
def task_success_handler(sender=None, result=None, **kwargs):
    if callback_manager:
        callback_manager.task_success_handler(sender, result, **kwargs)


def task_failure_handler(sender=None, exception=None, **kwargs):
    if callback_manager:
        callback_manager.task_failure_handler(sender, exception, **kwargs)