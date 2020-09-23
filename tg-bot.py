import dialogflow_v2 as dialogflow
import logging
import os
import telegram
import time
from functools import partial
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from dotenv import load_dotenv


logger = logging.getLogger()


class MyLogsHandler(logging.Handler):
  def __init__(self, logging_bot, chat_id):
    super().__init__()
    self.chat_id = chat_id
    self.logging_bot = logging_bot

  def emit(self, record):
    log_entry = self.format(record)
    self.logging_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_text(project_id, session_id, text, language_code='ru'):
  session_client = dialogflow.SessionsClient()
  session = session_client.session_path(project_id, session_id)
  text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
  query_input = dialogflow.types.QueryInput(text=text_input)
  response = session_client.detect_intent(session=session, query_input=query_input)
  fulfillment_text = response.query_result.fulfillment_text

  return fulfillment_text


def start(bot, update):
  update.message.reply_text('Здравствуйте, чем могу помочь?')


def respond(bot, update, project_id):
  session_id = f'tg-{update.message.from_user.id}'
  query_text = update.message.text
  response = detect_intent_text(project_id, session_id, query_text)
  update.message.reply_text(response)


def display_error(bot, update, error):
  logger.warning('Update "%s" caused error "%s"', update, error)


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
