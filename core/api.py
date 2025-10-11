import requests
from backend import settings

def send_teams_message(token, message):
    url = "https://graph.microsoft.com/v1.0/teams/" + settings.TEAM_ID + "/channels/" + settings.CHANNEL_ID + "/messages"
    data = {
        'body': {
            'content': message
        }
    }

    requests.post(url=url, json=data, headers={'Authorization': 'Bearer ' + token})