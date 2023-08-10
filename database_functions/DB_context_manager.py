import psycopg2
from settings import get_logger

logger = get_logger(__name__)


class UseDataBase:
    def __init__(self, db_config):
        self.configuration = db_config

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self.configuration['host'],
                port=self.configuration['port'],
                user=self.configuration['user'],
                password=self.configuration['password'],
                database=self.configuration['database'],
            )
            self.cursor = self.conn.cursor()
            return self.cursor

        except psycopg2.Error as e:
            logger.error(f"Error connecting to the database: {e}")
            raise  # Reraise the exception to propagate it

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.cursor.close()
        self.conn.close()

        if exc_type is not None:
            logger.error(f"Error occurred during database operation: {exc_val}")
