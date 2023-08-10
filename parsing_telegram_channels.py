import os
import time
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from settings import get_logger

logger = get_logger(__name__)


async def parsing(group_url: str, client: TelegramClient) -> list:
    list_dict = []
    # Собираем историю сообщений
    history = await client(GetHistoryRequest(
        peer=group_url,
        offset_id=0,
        offset_date=None, add_offset=0,
        limit=20, max_id=0, min_id=0,
        hash=0))
    if not history.messages:
        return list_dict
    messages = history.messages
    for message in messages:
        message_dict = message.to_dict()
        dict_data = dict()
        dict_data['id'] = message_dict.get('id')
        if message_dict.get('from_id', ):
            dict_data['from_id'] = message_dict.get('from_id').get('user_id')
        else:
            dict_data['from_id'] = None
        if message_dict.get('peer_id'):
            dict_data['peer_id'] = message_dict.get('peer_id').get('user_id')
            dict_data['channel_id'] = message_dict.get('peer_id').get('channel_id')

        dict_data['date'] = message_dict.get('date')
        dict_data['message'] = message_dict.get('message')
        dict_data['grouped_id'] = message_dict.get('grouped_id')
        if message_dict.get('media'):
            if message_dict.get('media').get('photo'):
                dict_data['photo_id'] = message_dict.get('media').get('photo').get('id')
            else:
                dict_data['photo_id'] = None
        list_dict.append(dict_data)
    return list_dict


def parsing_info_from_channels(list_urls: list) -> list:
    API_ID = int(os.getenv('api_id'))
    API_HASH = os.getenv('api_hash')
    all_list_dict = []
    # Создаем новый экземпляр TelegramClient используя существующую сессию.
    try:
        client = TelegramClient('x', API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
    except Exception as error:
        logger.error(error)
        return all_list_dict

    with client:

        try:
            for count, url in enumerate(list_urls):
                list_dict = client.loop.run_until_complete(parsing(url, client))
                all_list_dict.append(list_dict)

                time.sleep(30)
                logger.debug(f'собраны данные из канала {url}')
                logger.info(f'осталось собрать информацию из:{len(list_urls) - int(count)} каналов')
        except Exception as error:
            logger.error(error)

    return all_list_dict


if __name__ == '__main__':
    pass
