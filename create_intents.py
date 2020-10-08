import json
import dialogflow_v2
import os
from dotenv import load_dotenv


load_dotenv()
project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

intents = {}

with open('questions.json', 'r') as file:
  questions = json.load(file)

for topic, topic_questions in questions.items():
  intents[topic] = {
      'display_name': topic,
      'messages': [{
          'text':
          {'text': [topic_questions['answer']]}
      }],
      'training_phrases': []
  }

for topic, intent in intents.items():
  intent_questions = questions[topic]['questions']

  for question in intent_questions:
    intent['training_phrases'].append(
        {
            'parts': [{"text": question}]
        }
    )

'''
Creating intents
'''
client = dialogflow_v2.IntentsClient()

parent = client.project_agent_path(project_id)

for intent in intents.values():
  response = client.create_intent(parent, intent)

'''
Training agent
'''
client = dialogflow_v2.AgentsClient()

parent = client.project_path(project_id)

response = client.train_agent(parent)


def callback(operation_future):
  # Handle result.
  result = operation_future.result()


response.add_done_callback(callback)
