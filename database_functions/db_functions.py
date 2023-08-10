import os
import datetime
import psycopg2
from settings import get_logger
from database_functions.DB_context_manager import UseDataBase

logger = get_logger(__name__)

db_config = {
    'host': os.getenv('host'),
    'port': os.getenv('port'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'database': os.getenv('database')
}
table = os.environ.get('table')


def check_exist_table():
    sql_query = f"""SELECT EXISTS 
    (
    SELECT FROM 
        information_schema.tables 
    WHERE 
        table_schema LIKE 'public' AND 
        table_type LIKE 'BASE TABLE' AND
        table_name = '{table}'
    );"""
    try:
        with UseDataBase(db_config) as cursor:
            cursor.execute(sql_query)
            if cursor.fetchone()[0]:
                return True


    except psycopg2.Error as error:
        logger.error(f"Error: {error}")


def create_table():
    sql_query = f"""CREATE TABLE {table} (
                    id_ SERIAL PRIMARY KEY,
                    id INT,
                    from_id TEXT,
                    peer_id TEXT,
                    channel_id INT,
                    date TIMESTAMPTZ,
                    message TEXT,
                    grouped_id TEXT,
                    photo_id TEXT,
                    published BOOLEAN NOT NULL DEFAULT FALSE,
                    CONSTRAINT unique_messages UNIQUE (id, channel_id)
                    );"""

    try:
        with UseDataBase(db_config) as cursor:
            cursor.execute(sql_query)
    except psycopg2.Error as error:
        logger.error(f"Error: {error}")


def save_data_to_database(list_dict: list):
    if check_exist_table() is not True:
        create_table()
    for count, list_data in enumerate(list_dict):
        for data in list_data:
            sql_query = f"""INSERT INTO {table} (id, from_id, peer_id, channel_id, date, message, grouped_id, photo_id) 
            VALUES('{data.get("id")}','{data.get("from_id")}','{data.get("peer_id")}','{data.get("channel_id", 0)}',
            '{data.get("date")}','{data.get("message")}','{data.get("grouped_id")}','{data.get("photo_id")}' );"""
            try:
                with UseDataBase(db_config) as cursor:
                    cursor.execute(sql_query)
                    logger.info(f'Записали в БД: {count}, осталось записать: {len(list_dict) - count}')
            except psycopg2.Error as error:
                logger.error(f"Error: {error}")


def get_today_unpublished_message():
    list_messages = []
    # Получаем список неопубликованных сообщений с текущей датой содержащих текст
    sql_query = f"""SELECT id, channel_id FROM {table} 
    WHERE published = false AND message != '' AND date >= now()::date;"""
    try:
        with UseDataBase(db_config) as cursor:
            cursor.execute(sql_query)
            list_messages = cursor.fetchall()
    except psycopg2.Error as error:
        logger.error(f"Error: {error}")
    return list_messages


def update_flag_published(id: int, channel_id: int):
    sql_query = f"""UPDATE {table} SET published='TRUE' WHERE id={id} AND channel_id={channel_id};"""
    try:
        with UseDataBase(db_config) as cursor:
            cursor.execute(sql_query)
    except psycopg2.Error as error:
        logger.error(f"Error: {error}")


if __name__ == '__main__':
    pass
