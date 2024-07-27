from typing import Tuple

from flask import Blueprint, request, jsonify, Response
from ..core.task_manager import TaskManager
import logging

logger = logging.getLogger(__name__)


def create_routes(task_manager: TaskManager) -> Blueprint:
    bp = Blueprint('api', __name__)

    @bp.route('/run-task', methods=['POST'])
    def run_task() -> Tuple[Response, int]:
        # TODO: Add input validation
        try:
            task_name: str = request.json['task_name']
            task_parameters: dict = request.json['task_parameters']
            
            task_uuid: str = task_manager.create_task(task_name, task_parameters)
            
            return jsonify({'task_uuid': task_uuid}), 200
        
        except Exception as e:
            logger.exception("Error in run_task")
            return jsonify({'error': str(e)}), 500

    @bp.route('/get-task-output', methods=['GET'])
    def get_task_output() -> Tuple[Response, int]:
        try:
            task_uuid: str = request.args.get('task_uuid')
            
            output = task_manager.get_task_output(task_uuid)
            
            if output is None:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify({'task_output': output}), 200
        
        except Exception as e:
            logger.exception(f"Error in get_task_output. Error: {str(e)}")
            return jsonify({'Error': 'Internal Server Error'}), 500

    return bp
