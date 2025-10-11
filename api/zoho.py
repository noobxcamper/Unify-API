from requests import post
from core.models import ZohoToken
from backend.settings import ZOHO_SECRET_KEY, ZOHO_CLIENT_ID
import json, time, logging

def refresh_token(token):
    api_endpoint = 'https://accounts.zoho.com/oauth/v2/token'
    params = {
        'refresh_token': token,
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_SECRET_KEY,
        'redirect_uri': 'https://unify.experiorheadoffice.ca',
        'grant_type': 'refresh_token'
    }

    return post(api_endpoint, params=params)

def get_valid_token():
    token = ZohoToken.objects.first()
    
    if token.expires_at - int(time.time()) < 60:
        print("Zoho access token expired, refreshing")
        
        response = refresh_token(token.refresh_token)
        json_data = json.loads(response.content)
        
        if response.status_code == 200:
            token.access_token = json_data.get('access_token')
            token.expires_at = int(time.time()) + 3600
            token.save()

            logging.info("Zoho access token refreshed, expires at : " + str(token.expires_at))
        else:
            logging.error("Unable to refresh Zoho access token : " + json_data)
    
    return token.access_token