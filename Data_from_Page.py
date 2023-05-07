from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN = 'EAAIqlVvyJKcBAJHmfTqS2MYnVCvds257lL6tgGgQg1itzKqGkY2XdT7dtJqUjjoZAyxeVe7ZCbLTbPmOMlDeq2DLrWpe0pGZAL1y4XqksIS2TZClNQCzyMR0RjZCX1WzVGDmuBYPC7Ln0A4EcWzNGJtlyPY2syMaUarRTX4EBvFmbjWH2Q52ytnfNe0ZBYBCMkiNw8txpfAAZDZD'
    payload = {
        'recipient': {'id': senderPsid},
        'message': response,
        'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}
    url = 'https://graph.facebook.com/me/messages?access_token={}'.format(
        PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)


def handleMessage(senderPsid, receivedMessage):

    if 'text' in receivedMessage:
        response = {"text": "You sent me {}".format(receivedMessage['text'])}

        callSendAPI(senderPsid, response)
    else:
        response = {"text": "This chatbot only accept text msgs"}
        callSendAPI(senderPsid, response)


@app.route('/', methods=["GET", "POST"])
def home():
    return 'HOME'


@app.route('/webhook', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        VERIFY_TOKEN = 'EAAIqlVvyJKcBAGOR77bnGHdnH4sHrJzsRJHd0nu1Vnf8nCsOlIeBkuz6q0esbBXZCeaEFXViZCQSSFuZBidhnw5yhRIZCtaTzehDzyjgw3r82rITk6NiKKZCoZBsZBZAcVwzwGepTZAdeQqgXK7mfpZC7DsaVbbbRWbnQQDHBx0iiO5ZBIV4nG4zPlVHol6XO30QByTpZCqcEZC6P6QZDZD'
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK_VERIFIED')
                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                return 'ERROR', 403
        return 'SOMETHING', 200
    if request.method == 'POST':

        VERIFY_TOKEN = "EAAIqlVvyJKcBAJHmfTqS2MYnVCvds257lL6tgGgQg1itzKqGkY2XdT7dtJqUjjoZAyxeVe7ZCbLTbPmOMlDeq2DLrWpe0pGZAL1y4XqksIS2TZClNQCzyMR0RjZCX1WzVGDmuBYPC7Ln0A4EcWzNGJtlyPY2syMaUarRTX4EBvFmbjWH2Q52ytnfNe0ZBYBCMkiNw8txpfAAZDZD"
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK_VERIFIED')
                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                return 'ERROR', 403
        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port='3283', debug=True)
