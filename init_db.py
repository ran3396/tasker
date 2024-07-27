from app import create_app
from app.core.database_manager import DatabaseManager

app = create_app('development')


def init_db():
    # Initialize the tasks table in the database
    with app.app_context():
        db_manager = DatabaseManager(app.config)
        db_manager.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                uuid UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                parameters JSONB NOT NULL,
                status VARCHAR(50) NOT NULL,
                output JSONB
            )
        """)
        print("Database initialized successfully")


if __name__ == "__main__":
    init_db()
