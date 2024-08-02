import json
import boto3
from spotipy.oauth2 import SpotifyOAuth

def lambda_handler(event, context):
    CLIENT_ID = 'a080d421c6ab4b699ba470cb9d43f2d1'
    CLIENT_SECRET = 'dd52e8e1a1d8400a8779dbddf7da1c3e'
    REDIRECT_URI = 'YOUR_API_GATEWAY_URL/redirect'  # Replace with your API Gateway URL

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

    auth_url = sp_oauth.get_authorize_url()
    return {
        'statusCode': 302,
        'headers': {
            'Location': auth_url
        }
    }
