import tweepy
import math
import os
from dotenv import load_dotenv
load_dotenv()

def free_slots(api):
    print("free_slots")
    try:
        status = api.rate_limit_status(resources="statuses")
        remaining_resource = status['resources']['statuses']['/statuses/user_timeline']['remaining']
        slots = math.floor(remaining_resource/26)
        print(slots)
    except: 
        slots = 0
    return slots



def all_remaining_slots():
    global api
    bearer_token1 = os.getenv('BEARER_TOKEN')
    bearer_token2 = os.getenv('SECONDARY_BEARER_TOKEN')

    auth1 = tweepy.OAuth2BearerHandler(bearer_token1)
    auth2 = tweepy.OAuth2BearerHandler(bearer_token2)

    api1 = tweepy.API(auth1)
    api2 = tweepy.API(auth2)

    slots1 = free_slots(api1)
    slots2 = free_slots(api2)
    print('slots1: ',slots1)
    print('slots2: ',slots2)
    if slots1 > slots2:
        api = api1
    else:
        api = api2
    return slots1 + slots2


def getTimeline(screen_name, num_of_pages):
    timeline = []
    try:
        res = tweepy.Cursor(api.user_timeline, screen_name=screen_name,
                            count=200).pages(num_of_pages)
        for page in res:
            for post in page:
                timeline.append(post)
    except:
        return 'private'
    return timeline


def getAvatars(ids):
    res = api.lookup_users(user_id=ids, include_entities=False)
    return {user.id_str:user.profile_image_url_https.replace("normal", "400x400")  for user in res}

def getUser(screen_name):
    print('user_id_log ', screen_name )
    try:
        res = api.lookup_users(screen_name=[screen_name], include_entities=False)
    except tweepy.errors.HTTPException:
        return 404
    except:
        return 'problem'
    return {
		"id": res[0].id_str,
		"screen_name": res[0].screen_name,
		"avatar": res[0].profile_image_url_https.replace("normal", "400x400"),
	}


