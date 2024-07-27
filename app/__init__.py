from flask import Flask
import logging

from .core.database_manager import DatabaseManager
from .core.cache_manager import CacheManager
from .core.task_manager import TaskManager
from .tasks.callbacks import initialize_callback_manager
from .api.routes import create_routes


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.{config_name}.{config_name.capitalize()}Config')
    
    # Initialize managers
    db_manager = DatabaseManager(app.config)
    cache_manager = CacheManager(app.config)
    initialize_callback_manager(db_manager, cache_manager)
    task_manager = TaskManager(app.config, db_manager, cache_manager)
    
    # Set up logging
    logging.basicConfig(level=app.config['LOG_LEVEL'],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='logs/app.log',
                        filemode='a')
    
    # Register blueprints
    app.register_blueprint(create_routes(task_manager))
    
    return app
