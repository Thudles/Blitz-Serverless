import json
import boto3
import time
from spotipy.oauth2 import SpotifyOAuth

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SpotifyTokens')

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
    except ClientError as e:
        print(e.response['Error']['Message'])

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
