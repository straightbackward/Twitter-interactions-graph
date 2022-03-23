import boto3
from datetime import datetime
import time
import asyncio
from decimal import Decimal

async def put_into_db(user, execution_time):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users_Log')
    response = table.put_item(
       Item={
            'datetime': str(datetime.now()),
            'user_id': user['id'],
            'screen_name': user['screen_name'],
            'execution_time': Decimal(str(execution_time))
        }
    )

# def put_into_db(user):
#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table('Users_Log')
#     response = table.put_item(
#        Item={
#             'datetime': str(datetime.now()),
#             'user_id': user['id'],
#             'screen_name': user['screen_name']
#         }
#     )



async def db_async_handler(user, execution_time):
    start = time.time()
    task = asyncio.create_task(put_into_db(user, execution_time))
    end = time.time()
    print(end - start)
    await task


