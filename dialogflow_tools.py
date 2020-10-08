import logging
import dialogflow_v2 as dialogflow


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

    return response
