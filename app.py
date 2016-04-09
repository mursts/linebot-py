import json
import logging
import requests
import os
from flask import Flask
from flask import request

app = Flask(__name__)
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello():
    return 'Hello'


channel_id = os.environ['CHANNEL_ID']
channel_secret = os.environ['CHANNEL_SECRET']
mid = os.environ['MID']

CHANNEL = '1383378250'
EVENT_TYPE = '138311608800106203'


@app.route('/bot/callback', methods=['POST'])
def callback():
    results = json.loads(request.data)['result']

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'X-Line-ChannelID': channel_id,
               'X-Line-ChannelSecret': channel_secret,
               'X-Line-Trusted-User-With-ACL': mid}

    endpoint = 'https://trialbot-api.line.me/v1/events'

    for result in results:
        payload = {'to': result['from'],
                   'toChannel': CHANNEL,
                   'eventType': EVENT_TYPE,
                   'content': result['content']}

        r = requests.post(endpoint, data=json.dumps(payload),
                          headers=headers)
        logging.debug(r.status_code)
        logging.debug(r.text)
        r.raise_for_status()


    return 'Hi linebot'


if __name__ == '__main__':
    app.run()
