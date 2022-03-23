from re import A
from api import *
from flask import abort
import boto3
from db import db_async_handler,put_into_db
import time 
import asyncio



def addRecord(interactions, screen_name, user_id, type):
    if (user_id in interactions):
        interactions[user_id][type] += 1
    else:
        interactions[user_id] = {
            "screen_name": screen_name,
            "id": user_id,
            "reply": 0,
            "retweet": 0,
            "like": 0,
            type: 1,
        }


def countReplies(interactions, timeline, screen_name):
    for post in timeline:
        if ( (post.in_reply_to_user_id_str is not None) and post.in_reply_to_screen_name.lower() != screen_name):
            addRecord(
                interactions,
                post.in_reply_to_screen_name,
                post.in_reply_to_user_id_str,
                "reply"
            );
        
    

def countRetweets(interactions, timeline, screen_name):
    for post in timeline:
        if (
            hasattr(post, 'retweeted_status') and
            hasattr(post.retweeted_status, 'user') and
            post.retweeted_status.user.screen_name.lower() != screen_name
        ):
            addRecord(
                interactions,
                post.retweeted_status.user.screen_name,
                post.retweeted_status.user.id_str,
                "retweet"
            )
      
   




def getInteractions(screen_name, num_of_pages):
    timeline = (getTimeline(screen_name, num_of_pages))
    if timeline == 'private':
        return 'private'
    interactions = {}

    countReplies(interactions, timeline, screen_name)
    countRetweets(interactions, timeline, screen_name)
    tally = []
    
    for id, interaction in interactions.items():
        total = 0
        total += interaction['reply'] * 1.1
        total += interaction['retweet'] * 1.3

        tally.append({
            "id": interaction['id'],
            "screen_name": interaction['screen_name'],
            "total": total,
        })

  
    tally = sorted(tally, key= lambda x: x['total'], reverse=True)
    
    return tally


def make_graph(user_screen_name):
    start = time.time()
    user = getUser(user_screen_name)
    if user == 404:
        print('abort 404')
        return {'error': 'The user does not exists.'}
    elif user == 'problem':
        print('abort 500')
        abort(500)
    # put_into_db(user)
    layer1 = getInteractions(user_screen_name.lower(), 4)[:30]
    if layer1 == 'private':
        return {'error': 'The user is private.'}
    nodes = {user["id"]: {"screen_name": user_screen_name, "layer": 1}}
    edges = []
    for i, node_l1 in enumerate(layer1):
        nodes[node_l1["id"]] = {"screen_name": node_l1['screen_name'], "layer": 2}
        edges.append({"from": user_screen_name, "to": node_l1['screen_name']})
        if i<11:
            interactions = getInteractions(node_l1['screen_name'].lower(), 2)[:15]
            if interactions == 'private':
                continue
            for node_l2 in interactions:
                if node_l2["id"] not in nodes:
                    nodes[node_l2["id"]] = {"screen_name": node_l2['screen_name'], "layer": 3}
                edges.append({"from": node_l1['screen_name'], "to": node_l2['screen_name']})
    
    print('before pruning: ',len(nodes.keys()))
    for key in list(nodes.keys()):
        #remove nodes with degree 0 (pruning)
        degree = 0
        for edge in edges:
            if edge["to"] == nodes[key]["screen_name"] or edge["from"] == nodes[key]["screen_name"]:
                degree +=1
        if degree <= 1:
            del nodes[key]
            continue
    if len(nodes) == 0:
        return {'error': 'Your interactions rate is too low to make a graph.'}
    print('after pruning: ',len(nodes.keys()))
    avatars = getAvatars(nodes.keys())
    for key in list(nodes.keys()):
        # change key name "screen_name" to "id" to use the array straightforward in front
        nodes[key]["id"] = nodes[key]["screen_name"]
        del nodes[key]["screen_name"]
        
        # add avatars
        try:
            nodes[key]["image"] = avatars[key]
        except:
            del nodes[key]

        
    end = time.time()
    execution_time = end - start
    print('execution time: ', execution_time)
    asyncio.run(db_async_handler(user, round(execution_time, 2)))

    return {
        "nodes": list(nodes.values()),
        "edges": edges
    }
