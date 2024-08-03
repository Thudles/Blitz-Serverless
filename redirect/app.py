import json
import boto3
import time
from spotipy.oauth2 import SpotifyOAuth

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SpotifyTokens')

AWS_Region = "us-east-1"
ssm_client = boto3.client("ssm", region_name=AWS_Region)

CLIENT_ID = ssm_client.get_parameter(Name = "/spotifyapp/client_id", WithDecreption= True)
CLIENT_SECRET = ssm_client.get_parameter(Name = "/spotifyapp/client_secret", WithDecreption= True)
REDIRECT_URI = 'YOUR_API_GATEWAY_URL/redirect'  # Replace with your API Gateway URL


def store_token(user_id, token_info):
    try:
        table.put_item(
            Item={
                'user_id': user_id,
                'access_token': token_info['access_token'],
                'refresh_token': token_info['refresh_token'],
                'expires_at': int(time.time()) + token_info['expires_in']
            }
        )
    except:
        return None

def lambda_handler(event, context):
    

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

    code = event['queryStringParameters']['code']
    token_info = sp_oauth.get_access_token(code)
    
    user_id = 'some_unique_user_id'  # Replace with a method to get a unique user ID

    store_token(user_id, token_info)

    return {
        'statusCode': 302,
        'headers': {
            'Location': 'YOUR_API_GATEWAY_URL/friendsPlaylist'  # Replace with your API Gateway URL
        }
    }
