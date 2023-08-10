import os
import time
from telethon import TelegramClient
from database_functions.db_functions import get_today_unpublished_message, update_flag_published
from settings import get_logger

logger = get_logger(__name__)


async def posting(client: TelegramClient, target_chat: str) -> None:
    # Получаем данные не опубликованных сообщений с текущей датой
    list_messages = get_today_unpublished_message()
    for count, message in enumerate(list_messages):
        message_id = message[0]
        from_chat = message[1]
        # Для пересылки сообщения указываем урл цевого чата, id пересылаемого сообщения, id чата исходника.
        await client.forward_messages(target_chat, message_id, from_chat)
        time.sleep(10)
        update_flag_published(message_id, from_chat)
        logger.info(f'Осталось опубликовать сообщений: {len(list_messages) - count}')


def posting_main():
    API_ID = int(os.getenv('api_id'))
    API_HASH = os.getenv('api_hash')

    # Создаем новый экземпляр TelegramClient используя существующую сессию.

    client = TelegramClient('x', API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")

    with client:
        client.loop.run_until_complete(posting(client, os.getenv('target_chat')))


if __name__ == '__main__':
    posting_main()
    pass
