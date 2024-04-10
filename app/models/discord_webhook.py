import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = config['DEFAULT']['DISCORD_WEBHOOK_URL']

    def send_message(self, message):
        data = {
            'content': message
        }
        requests.post(self.webhook_url, data=data)