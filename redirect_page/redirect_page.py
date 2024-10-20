import json
import boto3
from spotipy import SpotifyOAuth

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourDynamoDBTableName')

def lambda_handler(event, context):
    code = event['queryStringParameters']['code']
    sp_oauth = SpotifyOAuth(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', redirect_uri="https://your-api-gateway-url/redirect")
    token_info = sp_oauth.get_access_token(code)
    
    # Store token info in DynamoDB
    table.put_item(Item={
        'user_id': token_info['user_id'],
        'token_info': token_info
    })
    
    return {
        'statusCode': 302,
        'headers': {
            'Location': 'https://your-api-gateway-url/friendsPlaylist'
        }
    }
