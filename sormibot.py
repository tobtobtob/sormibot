from flask import Flask, request
import requests
import os
app = Flask(__name__)

secret = os.environ['secret']
bot_id = os.environ['bot_id']
send_message_url = "https://api.telegram.org/bot" + bot_id + "/sendMessage"
niksi_url = os.environ['niksi_url']

@app.route("/")
def testing():
    return "Sormibotti vastaa!"

@app.route("/"+secret, methods=['POST'])
def handleMessage():
    message_json = request.get_json()
    text_message = message_json['message']['text']
    chat_id = message_json['message']['chat']['id']
    sender_name = message_json['message']['from']['first_name']

    if text_message == "/moro":
        requests.get(send_message_url, params = {'chat_id' : chat_id, 'text': "moro " + sender_name + " :D"})

    if text_message == "/niksi":
        niksi_response = requests.get(niksi_url)
        requests.get(send_message_url, params = {'chat_id' : chat_id, 'text': niksi_response.text})

    return "Viesti käsitelty"

