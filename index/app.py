import json
import boto3
from spotipy.oauth2 import SpotifyOAuth

AWS_Region = "us-east-1"
ssm_client = boto3.client("ssm", region_name=AWS_Region)

def lambda_handler(event, context):
    CLIENT_ID = ssm_client.get_parameter(Name = "/spotifyapp/client_id", WithDecreption= True)
    CLIENT_SECRET = ssm_client.get_parameter(Name = "/spotifyapp/client_secret", WithDecreption= True)
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
