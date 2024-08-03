import json
import boto3
import spotipy
import time
import execjs
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

def get_token(user_id):
    
    try:
        response = table.get_item(
            Key={
                'user_id': user_id
            }
        )
        
        token_info = response['Item']
    
        if not token_info:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': 'YOUR_API_GATEWAY_URL/'  # Replace with your API Gateway URL
                }
            }
        
        now = int(time.time())
        
        if token_info['expires_at'] - now < 60:
            spotify_oauth = SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri='YOUR_API_GATEWAY_URL/redirect',  # Replace with your API Gateway URL
                scope='user-library-read playlist-modify-public playlist-modify-private'
            )
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
            store_token(user_id, token_info)
        
        return token_info
        
    except:
        print("e.response['Error']['Message']")
        return None


def lambda_handler(event, context):
    
    # Load the JavaScript file
    with open('script.js', 'r') as file:
        js_code = file.read()

    # Create a runtime context with the loaded JavaScript code
    context = execjs.compile(js_code)

    # Execute JavaScript code
    context.call("main")
    
    user_id = 'some_unique_user_id'  # Replace with a method to get a unique user ID

    token_info = get_token(user_id)  # Retrieve the token_info from storage
    
    if not token_info:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': 'YOUR_API_GATEWAY_URL/'  # Replace with your API Gateway URL
                }
            }

    sp = spotipy.Spotify(auth=token_info['access_token'])

    with open('uris.txt', 'r') as file:
        song_uris = [line.strip() for line in file]

    current_user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=current_user_id, name='Blitz', public=False)
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

    return {
        'statusCode': 200,
        'body': json.dumps('SUCCESS!!!')
    }
