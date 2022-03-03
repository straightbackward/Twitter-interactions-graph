import resource
import requests
import json
import logging
import time
import tweepy
import math
import os
# os.environ['http_proxy'] = 'http://127.0.0.1:33977'
# os.environ['https_proxy'] = 'http://127.0.0.1:33977' 


auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAEDVPgEAAAAAml%2FCoV9VHPYULHiwF5%2FZJZOn3OQ%3DLMmUgmLlGq7pGWqur9GBdVxBuZrDZhOm3pn9ZvH9oT7yMdbf7O")


api = tweepy.API(auth)


def getTimeline(screen_name, num_of_pages):
    timeline = []
    try:
        res = tweepy.Cursor(api.user_timeline, screen_name=screen_name,
                            count=200).pages(num_of_pages)
        for page in res:
            print(len(page))
            for post in page:
                timeline.append(post)
     
    except:
        return 'private'
    return timeline


def getAvatars(ids):
    res = api.lookup_users(user_id=ids, include_entities=False)
    return {user.id_str:user.profile_image_url_https.replace("normal", "400x400")  for user in res}

def getUser(screen_name):
    print('id ', screen_name )
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



def free_slots():
    status = api.rate_limit_status(resources="statuses")
    remaining_resource = status['resources']['statuses']['/statuses/user_timeline']['remaining']
    return math.floor(remaining_resource/26)

