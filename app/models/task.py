from typing import Optional, Dict, Any
import json
from ..core.database_manager import DatabaseManager


class Task:
    def __init__(self, uuid: str, name: str, parameters: Dict[str, Any], status: str, output: Optional[Dict[str, Any]] = None) -> None:
        self.uuid: str = uuid
        self.name: str = name
        self.parameters: Dict[str, Any] = parameters
        self.status: str = status
        self.output: Optional[Dict[str, Any]] = output

    @classmethod
    def create(cls, db_manager: DatabaseManager, task_uuid: str, name: str, parameters: Dict[str, Any]) -> 'Task':
        db_manager.execute(
            "INSERT INTO tasks (uuid, name, parameters, status) VALUES (%s, %s, %s, %s)",
            (task_uuid, name, json.dumps(parameters), 'PENDING')
        )
        return cls(task_uuid, name, parameters, 'PENDING')

    @classmethod
    def get(cls, db_manager: DatabaseManager, task_uuid: str) -> Optional['Task']:
        result = db_manager.execute("SELECT * FROM tasks WHERE uuid = %s", (task_uuid, ))
        if result:
            task = result[0]
            return cls(
                task['uuid'],
                task['name'],
                task['parameters'],
                task['status'],
                task['output'] if task['output'] else None
            )
        return None

    def update_status(self, db_manager: DatabaseManager, status: str, output: Optional[Dict[str, Any]] = None) -> None:
        db_manager.execute(
            "UPDATE tasks SET status = %s, output = %s WHERE uuid = %s",
            (status, json.dumps(output) if output else None, self.uuid)
        )
        self.status = status
        self.output = output
