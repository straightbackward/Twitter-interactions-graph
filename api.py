import requests
import os
import json
import logging
import time
import tweepy
import os
os.environ['http_proxy'] = 'http://127.0.0.1:33977'
os.environ['https_proxy'] = 'http://127.0.0.1:33977' 







consumer_key = "Fg5AoQNjh7vAGbD1335DpUI3f"
consumer_secret = "QX8miw5x5Z8BMrLAX3GMn0d7oQ6GpxoxkbhMerz3DYY690FMkQ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)


api = tweepy.API(auth)


def getTimeline(screen_name, num_of_pages):
    timeline = []
    res = tweepy.Cursor(api.user_timeline, screen_name=screen_name,
                            count=200).pages(num_of_pages)
    for page in res:
        print(len(page))
        for post in page:
            timeline.append(post)
     
    
    return timeline


def getAvatars(ids):
    res = api.lookup_users(user_id=ids, include_entities=False)
    return {user.id_str:user.profile_image_url_https.replace("normal", "400x400")  for user in res}

def getUser(screen_name):
    res = api.lookup_users(screen_name=screen_name, include_entities=False)
    return {
		"id": res[0].id_str,
		"screen_name": res[0].screen_name,
		"avatar": res[0].profile_image_url_https.replace("normal", "400x400"),
	}
    
# print(getAvatars('vaslolkhetab, hamed'))
