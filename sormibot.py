from flask import Flask, request
import requests
import os
app = Flask(__name__)

secret = os.environ['secret']
bot_id = os.environ['bot_id']
send_message_url = "https://api.telegram.org/bot" + bot_id + "/sendMessage"
send_video_url = "https://api.telegram.org/bot" + bot_id + "/sendMessage"
niksi_url = os.environ['niksi_url']
giphy_api_key = os.environ['giphy_api_key']
giphy_url = "http://api.giphy.com/v1/gifs/random?api_key=" + giphy_api_key


@app.route("/")
def testing():
    return "Sormibotti vastaa!", 200

@app.route("/"+secret, methods=['POST'])
def handleMessage():
    message_json = request.get_json()
    text_message = message_json['message']['text']
    chat_id = message_json['message']['chat']['id']
    sender_name = message_json['message']['from']['first_name']

    if text_message == "/moro":
        send_message(chat_id, "moro " + sender_name + " :D")

    elif text_message == "/niksi":
        niksi_response = requests.get(niksi_url)
        send_message(chat_id, niksi_response.text)

    elif "/shitpost" in text_message:
        if len(text_message.split()) <= 1:
            gif_url = getRandomGif()
            send_video(chat_id, gif_url)
        elif len(text_message.split()) == 2 and text_message.split()[1].isdigit():
            number_of_posts = int(text_message.split()[1])
            for x in range(0, min(number_of_posts, 10)):
                gif_url = getRandomGif()
                send_video(chat_id, gif_url)
        else:
            not_a_command(chat_id)

    elif text_message == "/pekka":
        send_message(chat_id, "VASTAA")

    else:
        not_a_command(chat_id)

    return "Ok", 200

def not_a_command(chat_id):
    send_message(chat_id, "En ymmärtänyt komentoa")

def getRandomGif():
    r = requests.get(giphy_url)
    print("URL:::::  " + r.json()['data']['embed_url'])
    return r.json()['data']['images']['fixed_height']['url']

def send_message(chat_id, text):
    send_message_url = "https://api.telegram.org/bot" + bot_id + "/sendMessage"
    requests.get(send_message_url, params = {'chat_id' : chat_id, 'text': text})

def send_video(chat_id, video_url):
    send_video_url = "https://api.telegram.org/bot" + bot_id + "/sendVideo"
    r = requests.get(send_video_url, params = {'chat_id' : chat_id, 'video' : video_url})
