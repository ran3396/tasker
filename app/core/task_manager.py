from typing import Dict, Any, Optional
from celery import Celery
from celery.result import AsyncResult
import json
import logging
from flask import Config

from ..models.task import Task
from .database_manager import DatabaseManager
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, config: Config, db_manager: DatabaseManager, cache_manager: CacheManager) -> None:
        self.config: Config = config
        self.db_manager: DatabaseManager = db_manager
        self.cache_manager: CacheManager = cache_manager
        self.celery: Celery = Celery(__name__)
        self.celery.conf.update(config)

    def create_task(self, task_name: str, task_parameters: Dict[str, Any]) -> str:
        # Create a new task based on the task name and parameters provided, and send it to Celery for execution
        # The task UUID returned can be used to query the status and output of the task
        if task_name == 'sum_two_numbers':
            celery_task = self.celery.send_task('app.tasks.task_functions.sum_two_numbers', 
                                                args=[task_parameters['a'], task_parameters['b']])
        elif task_name == 'query_chatgpt':
            celery_task = self.celery.send_task('app.tasks.task_functions.query_chatgpt', 
                                                args=[task_parameters['prompt'], self.config['OPENAI_API_KEY']])
        elif task_name == 'find_longest_consecutive_letters':
            celery_task = self.celery.send_task('app.tasks.task_functions.find_longest_consecutive_letters',
                                                args=[task_parameters['string']])
        else:
            logger.error(f"Invalid task name: {task_name}")
            raise ValueError("Invalid task name")

        task_uuid = celery_task.id
        task = Task.create(self.db_manager, task_uuid, task_name, task_parameters)

        logger.info(f"Task created: {task.uuid}")
        return task.uuid

    def get_task_output(self, task_uuid: str) -> (Dict[str, Any], ):
        # Get the status and output of a task based on the task UUID
        # First, try to get the output from the cache, if not found, get it from the database
        logger.info(f"Fetching output for task: {task_uuid}")

        # Try to get from cache first
        cache_key = f'celery-task-meta-{task_uuid}'
        cached_output = self.cache_manager.get(cache_key)
        if cached_output:
            logger.info(f"Cache hit for task: {task_uuid}")
            task_meta = json.loads(cached_output)
            return {
                'status': 'COMPLETED' if task_meta['status'] == 'SUCCESS' else 'FAILED',
                'result': task_meta['result'] if task_meta['status'] == 'SUCCESS' else None,
                'error': task_meta['result'] if task_meta['status'] == 'FAILURE' else None
            }

        # If not in cache, get from database
        task = Task.get(self.db_manager, task_uuid)
        if task is None:
            logger.warning(f"Task not found in database: {task_uuid}")
            return None

        return {
            'status': task.status,
            'result': task.output if task.status == 'COMPLETED' else None,
            'error': task.output.get('error') if task.status in ['FAILED', 'ERROR'] else None
        }
