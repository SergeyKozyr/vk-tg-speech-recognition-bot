import vk_api
import os
import random
import telegram
import logging
import time
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_tools import MyLogsHandler, detect_intent_text


logger = logging.getLogger()


def respond(event, vk_api, text):
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    telegram_logging_bot_token = os.getenv('TG_LOGGING_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    vk_community_token = os.getenv('VK_COMMUNITY_TOKEN')
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    logging_bot = telegram.Bot(token=telegram_logging_bot_token)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(logging_bot, chat_id))
    logger.info('Бот vk-speech-recognition запущен')

    vk_session = vk_api.VkApi(token=vk_community_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    session_id = f'vk-{event.user_id}'
                    response = detect_intent_text(project_id, session_id, event.text)
                    intent_is_fallback = response.query_result.intent.is_fallback
                    text = response.query_result.fulfillment_text
                    if not intent_is_fallback:
                        respond(event, vk_api, text)

        except Exception:
            logger.exception('Бот vk-speech-recognition упал с ошибкой: ')
            time.sleep(10)
