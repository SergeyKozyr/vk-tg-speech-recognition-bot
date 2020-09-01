## Description

These are python scripts that use telegram and vkontakte bot api, to create support chat-bots.

Bots are trained with [Google's DialogFlow neural network](https://dialogflow.cloud.google.com/).

Each bot's logs are sent to Logging bot via telegram.

## Usage

Send a question ([available questions](https://gist.github.com/SergeyKozyr/e27114507c854c1d5d0f72e8c84591d9)) to [Telegram bot](https://t.me/dvmn_speech_recog_bot) or [VK group](https://vk.com/im?sel=-198272472)

## Example

**Vkontakte:**

![Vkontakte bot](https://github.com/SergeyKozyr/vk-tg-speech-recognition-bot/blob/media/vk-bot-example.gif?raw=true)

**Telegram:**

![Telegram bot](https://github.com/SergeyKozyr/vk-tg-speech-recognition-bot/blob/media/tg-bot-example.gif?raw=true)

## How to install

1) **Running on a local machine**

- Create .env file with the variables

        DIALOGFLOW_PROJECT_ID="Your dialogflow project id"
        GOOGLE_APPLICATION_CREDENTIALS="google credentials json file"
        TG_LOGGING_BOT_TOKEN="Logging bot telegram token"
        TG_BOT_TOKEN="Telegram bot token"
        TG_CHAT_ID="Your telegram chat id"
        VK_COMMUNITY_TOKEN="Your vk community token"

    - Create a [DialogFlow project](https://cloud.google.com/dialogflow/es/docs/quick/setup), and build an [agent](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)

    - Create intents

    - Create [google credentials json file](https://cloud.google.com/docs/authentication/getting-started)

    - Create [vk group](https://vk.com/groups), in your group click manage -> Api usage and generate an access token with community management and messages access settings

    - Telegram bot tokens are available after creation in @BotFather chat

    - For your chat id send, a message to @userinfobot 


- Install dependancies

        pip install -r requirements.txt

- Run script, send a message to the bot

        python vk-bot.py
        python tg-bot.py


2) **Deploying with Heroku**

- Clone the repository, sign up or log in at [Heroku](https://www.heroku.com/)

- Create a new Heroku app, click on Deploy tab and connect your Github

- Type in the repository name and click Deploy Branch at the bottom of the page

- Set up environment variables at the Settings tab in Config Vars, [add google credentials](https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku), use [this buildpack](https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack), as well as heroku's default python one 

- Turn on the 'bot' process on Resources tab


## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org)