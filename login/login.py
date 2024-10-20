import json
import boto3
from spotipy import SpotifyOAuth

def lambda_handler(event, context):
    client_id = 'CLIENT_ID'
    client_secret = 'CLIENT_SECRET'
    redirect_uri = "https://your-api-gateway-url/redirect"
    scope = 'user-library-read playlist-modify-public playlist-modify-private'
    
    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    
    return {
        'statusCode': 302,
        'headers': {
            'Location': auth_url
        }
    }
