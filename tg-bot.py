import logging
import os
import telegram
import time
from functools import partial
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from dotenv import load_dotenv
from dialogflow_tools import MyLogsHandler, detect_intent_text


logger = logging.getLogger()


def start(bot, update):
  update.message.reply_text('Здравствуйте, чем могу помочь?')


def respond(bot, update, project_id):
  session_id = f'tg-{update.message.from_user.id}'
  query_text = update.message.text
  response = detect_intent_text(project_id, session_id, query_text)
  update.message.reply_text(response.query_result.fulfillment_text)


def display_error(bot, update, error):
  logger.error('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
  load_dotenv()
  tg_bot_token = os.getenv('TG_BOT_TOKEN')
  telegram_logging_bot_token = os.getenv('TG_LOGGING_BOT_TOKEN')
  chat_id = os.getenv('TG_CHAT_ID')
  project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

  logging_bot = telegram.Bot(token=telegram_logging_bot_token)
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  logger.setLevel(logging.INFO)
  logger.addHandler(MyLogsHandler(logging_bot, chat_id))
  logger.info('Бот tg-speech-recognition запущен')

  updater = Updater(tg_bot_token)
  dispatcher = updater.dispatcher

  send_response = partial(respond, project_id=project_id)

  dispatcher.add_error_handler(display_error)
  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(MessageHandler(Filters.text, send_response))

  while True:
    try:
      updater.start_polling()
      updater.idle()

    except Exception:
      logger.exception('Бот tg-speech-recognition упал с ошибкой: ')
      time.sleep(10)
