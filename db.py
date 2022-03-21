import boto3
from datetime import datetime

def put_into_db(user):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users_Log')
    response = table.put_item(
       Item={
            'datetime': str(datetime.now()),
            'user_id': user['id'],
            'screen_name': user['screen_name']
        }
    )
