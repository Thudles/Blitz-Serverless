import json
import boto3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourDynamoDBTableName')

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']  # Get user id from auth
    response = table.get_item(Key={'user_id': user_id})

    if 'Item' not in response:
        return {
            'statusCode': 302,
            'headers': {
                'Location': 'https://your-api-gateway-url/'
            }
        }
    
    token_info = response['Item']['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Read song URIs from DynamoDB or another source
    song_uris = [...]  # Load your song URIs here
    
    current_user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=current_user_id, name='Blitz', public=False)
    
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
    
    return {
        'statusCode': 200,
        'body': json.dumps("SUCCESS!!!")
    }
