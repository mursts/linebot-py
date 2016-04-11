import base64
import json
import logging
import requests
import os
import hmac
import hashlib
from flask import Flask, request

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
    results = request.json

    logging.debug(results)

    channel_signature = request.headers['X-LINE-CHANNELSIGNATURE']
    hash = hmac.new(channel_secret.encode('utf-8'), request.data, hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode()

    if not hmac.compare_digest(channel_signature, signature):
        logging.error('signature validate is failed.')
        return 'signature validate is failed.'

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'X-Line-ChannelID': channel_id,
               'X-Line-ChannelSecret': channel_secret,
               'X-Line-Trusted-User-With-ACL': mid}

    proxies = {'https': os.environ['FIXIE_URL']}

    endpoint = 'https://trialbot-api.line.me/v1/events'

    for result in results['result']:
        payload = {'to': [result['content']['from']],
                   'toChannel': CHANNEL,
                   'eventType': EVENT_TYPE,
                   'content': {
                       'contentType': 1,
                       'toType': 1,
                       'text': "Hello"
                   }}

        r = requests.post(endpoint, data=json.dumps(payload),
                          headers=headers, proxies=proxies)
        logging.debug(r.status_code)
        logging.debug(r.text)
        r.raise_for_status()

    return 'Hi linebot'


if __name__ == '__main__':
    app.run()
