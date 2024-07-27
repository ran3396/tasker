# Asynchronous Task Management System

## Overview

This project is an asynchronous task management system built with Flask, Celery, Redis, and PostgreSQL. It provides a robust architecture for creating, executing, and managing long-running tasks in a scalable and efficient manner.

## Features

- RESTful API for task creation and status retrieval
- Asynchronous task execution using Celery
- Task result caching with Redis
- Persistent storage of task details in PostgreSQL
- Supports multiple task types (e.g., sum two numbers, query ChatGPT)
- Scalable architecture ready for horizontal scaling
- Comprehensive test suite with unit and integration tests
- Docker support for easy deployment and development

## Technology Stack

- **Flask**: Lightweight WSGI web application framework
- **Celery**: Asynchronous task queue/job queue based on distributed message passing
- **Redis**: In-memory data structure store, used as a message broker and result backend for Celery, and for caching
- **PostgreSQL**: Open-source relational database for persistent storage
- **psycopg2**: PostgreSQL adapter for Python
- **requests**: HTTP library for making API calls (used in ChatGPT task)
- **pytest**: Testing framework for Python
- **Docker**: Containerization platform for easy deployment and scaling

## Project Structure

```
task_app_project/
│
├── app/
│   ├── init.py
│   ├── api/
│   │   ├── init.py
│   │   └── routes.py
│   ├── core/
│   │   ├── init.py
│   │   ├── task_manager.py
│   │   ├── database_manager.py
│   │   └── cache_manager.py
│   ├── models/
│   │   ├── init.py
│   │   └── task.py
│   └── tasks/
│       ├── init.py
│       ├── callbacks.py
│       └── task_functions.py
├── config/
│   ├── init.py
│   ├── base.py
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_cache_manager.py
│   │   ├── test_database_manager.py
│   │   ├── test_task_manager.py
│   │   └── test_task_model.py
│   └── integration/
│       └── test_api.py
├── logs/
├── Dockerfile
├── pytest.ini
├── docker-compose.yml
├── init_db.py
├── run.py
├── celery_worker.py
└── requirements.txt
```

## Design Decisions and Rationale

1. **Modular Architecture**: The project is structured into modules (api, core, models, tasks) to promote separation of concerns and maintainability.

2. **Manager Classes**: We use manager classes (TaskManager, DatabaseManager, CacheManager) to encapsulate the logic for interacting with different components of the system. This promotes loose coupling and makes the system more testable and maintainable.

3. **Dependency Injection**: The manager classes are instantiated in the app factory and injected where needed, rather than being global instances. This makes the code more flexible and easier to test.

4. **Task Model**: We use a Task model to represent tasks in the system. This allows us to easily extend the properties of a task in the future if needed.

5. **Celery for Asynchronous Tasks**: Celery is used to handle asynchronous task execution. This allows the main application to remain responsive while long-running tasks are processed in the background.

6. **Redis for Caching and Message Broker**: Redis is used both as a cache for task results and as a message broker for Celery. This provides fast in-memory storage for frequently accessed data and efficient message passing for task queue management.

7. **PostgreSQL for Persistent Storage**: While Redis provides fast access to task data, PostgreSQL is used for persistent storage of all task information. This ensures data durability and allows for complex queries if needed in the future.

8. **Configurable Settings**: The use of a config module with different environments (base, development, production, testing) allows for easy configuration management across different deployment scenarios.

9. **Type Hinting**: We use type hints throughout the codebase to improve code readability and catch type-related errors early in the development process.

10. **Error Handling and Logging**: Error handling and logging are implemented to make debugging easier and to provide better visibility into the system's operation.

11. **Comprehensive Testing**: A comprehensive test suite using pytest, including unit tests and integration tests, ensures the reliability and correctness of the system.

12. **Docker Support**: Docker and Docker Compose configurations are provided for easy deployment and consistent development environments.

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/ran3396/tasker.git
cd tasker
```

2. Set up a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip3 install -r requirements.txt
```

3. Set up PostgreSQL:
- Install PostgreSQL
- Create a new database and user
- Update the database configuration in `config/base.py`

4. Set up Redis:
- Install Redis
- Start the Redis server
- Update the Redis configuration in `config/base.py` if necessary

5. Initialize the database:

```bash
python init_db.py
```

6. Start the Flask application:

```bash
  python run.py
```

7. Start Celery worker:

```bash
celery -A celery_worker.celery worker --loglevel=info
```

## API Endpoints

- `POST /run-task`: Create a new task
- Parameters:
 - `task_name`: Name of the task to run
 - `task_parameters`: Parameters for the task
- Returns: Task UUID
- Currently supported tasks:
  - `sum_two_numbers`: Add two numbers
    - Parameters:
      - `a`: First number
      - `b`: Second number
    - Example:
      ```json
      {
        "task_name": "sum_two_numbers",
        "task_parameters": {
          "a": 5,
          "b": 10
        }
      }
      ```
  - `query_chatgpt`: Query ChatGPT for a response
    - Parameters:
      - `prompt`: Prompt for ChatGPT
    - Example:
      ```json
      {
        "task_name": "query_chatgpt",
        "task_parameters": {
          "prompt": "Tell me a joke."
        }
      }
      ```
  - `find_longest_consecutive_letters`: Find the longest consecutive letters in a string
    - Parameters:
      - `string`: Input text
    - Example:
      ```json
      {
        "task_name": "find_longest_consecutive_letters",
        "task_parameters": {
          "string": "aaabbccccdd"
        }
      }
      ```


- `GET /get-task-output`: Get the output of a task
- Parameters:
 - `task_uuid`: UUID of the task
- Returns: Task output or status

## Example Usage using curl

1. Create a new task:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"task_name": "sum_two_numbers", "task_parameters": {"a": 5, "b": 10}}' http://localhost:5000/run-task
```
This will return a UUID for the task.

2. Get the output of the task:

```bash
curl -X GET http://localhost:5000/get-task-output?task_uuid=<task_uuid>
```


## Docker Setup

This project includes a Docker setup for easy deployment. To run the application using Docker:

1. Make sure Docker and Docker Compose are installed on your system.
2. Navigate to the project root directory.
3. Run the following command:

```bash
docker-compose up --build
```

This will build the Docker images and start all the services.

4. The application will be available at `http://localhost:5000`.

To stop the services, use:

```bash
docker-compose down
```

Note: The first time you run the services, the database will be initialized automatically. If you need to reinitialize the database, you can run:

```bash
  docker-compose run web python init_db.py
```

This Docker setup includes:
- The main Flask application
- A Celery worker
- PostgreSQL database
- Redis for caching and as a message broker

The Docker setup uses environment variables for configuration, making it easy to adjust settings for different environments.

## Running Tests

This project uses pytest for testing. To run the tests:

1. Make sure you have installed the required packages:

```bash
pip3 install -r requirements.txt
```

2. Run the tests using pytest:
    
```bash
python3 -m pytest
```

This will run all the tests in the `tests` directory. You can also run specific test files or functions by specifying them:

```bash
python3 -m pytest tests/unit/test_task_manager.py
```

The tests include both unit tests for individual components and integration tests for the API endpoints. Mocks are used to isolate components and test them independently.

## Future Improvements

1. Implement user authentication and authorization
2. Add more task types and make task registration dynamic
3. Implement task prioritization and advanced routing
4. Add monitoring and alerting for system health
5. Implement rate limiting to prevent abuse
6. Add support for task cancellation and pausing
7. Implement more advanced caching strategies
8. Improve the test coverage and add more integration tests
9. Make logging more robust and configurable
10. Implement a more advanced error handling system
11. Refactor the codebase for better modularity and maintainability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.