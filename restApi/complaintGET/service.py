""" POST for role.
"""
import uuid
import boto3
import time

def get_community(id, boto_client):
    key = {"id": {"S": id}}
    item = boto_client.get_item(TableName="communities",Key=key)
    community = {}
    community["id"] = id
    community["name"] = item.get("Item").get("name").get("S")
    return community   

def get_parks(ids, boto_client):
    parks = []
    for id in ids:
        key = {"id": id}
        item = boto_client.get_item(TableName="parks",Key=key)
        park = {}
        park ["id"] = item.get("Item").get("id").get("S")
        park ["name"] =  item.get("Item").get("name").get("S")
        park ["address"] = item.get("Item").get("address").get("S")
        park ["description"] = item.get("Item").get("description").get("S")
        park ["image_url"] = item.get("Item").get("image_url").get("S")
        park ["location"] = {}
        park ["location"]["lat"] = item.get("Item").get("location").get("M").get("lat").get("N")
        park ["location"]["long"] = item.get("Item").get("location").get("M").get("long").get("N")
        park ["community"] = get_community(item.get("Item").get("community").get("S"), boto_client)
        parks.append(park)
    return parks

def get_role(id, boto_client):
    key = {"id": {"S": id}}
    item = boto_client.get_item(TableName="roles",Key=key)
    role = {}
    role["id"] = id
    role["name"] = item.get("Item").get("name").get("S")
    return role    

def get_comments(ids, boto_client):
    comments = []
    for id in ids:
        key = {"id": id}
        item = boto_client.get_item(TableName="comments",Key=key)
        comment = {}
        comment["id"] = id.get("S")
        comment["description"] = item.get("Item").get("description").get("S")
        comment["time"] = item.get("Item").get("time").get("S")
        

        key = {"id": {"S": item.get("Item").get("user").get("S")}}
        try:
            user_item = boto_client.get_item(TableName="users",Key=key)
        except Exception, exception:
            return exception
        user = {}
        user ["id"] = user_item.get("Item").get("id").get("S")
        user ["name"] =  user_item.get("Item").get("name").get("S")
        user ["image_url"] = user_item.get("Item").get("image_url").get("S")
        user ["phone"] = user_item.get("Item").get("phone").get("S")
        user ["address"] = user_item.get("Item").get("address").get("S")
        user ["email"] = user_item.get("Item").get("address").get("S")
        user ["phone_token"] = user_item.get("Item").get("address").get("S")
        user ["time"] = user_item.get("Item").get("time").get("S")
        user ["location"] = {}
        user ["location"]["lat"] = user_item.get("Item").get("location").get("M").get("lat").get("N")
        user ["location"]["long"] = user_item.get("Item").get("location").get("M").get("long").get("N")
        user ["role"] = get_role(user_item.get("Item").get("role").get("S"), boto_client)
        user ["subscribed_parks"] = get_parks(user_item.get("Item").get("subscribed_parks").get("L"),boto_client)
        user ["supervised_parks"] = get_parks(user_item.get("Item").get("supervised_parks").get("L"),boto_client)
        comment["user"] = user


        comments.append(comment)
    return comments


def handler(event, context):
    client = boto3.client("dynamodb")
    key = {"id": {"S": event.get("id")}}
    try:
        item = client.get_item(TableName="complaints",Key=key)
    except Exception, exception:
        return exception
    complaint = {}
    complaint ["id"] = item.get("Item").get("id").get("S")
    complaint ["title"] =  item.get("Item").get("title").get("S")
    complaint ["image_url"] = item.get("Item").get("image_url").get("S")
    complaint ["description"] = item.get("Item").get("description").get("S")
    complaint ["last_updated"] = item.get("Item").get("last_updated").get("S")
    complaint ["time"] = item.get("Item").get("time").get("S")
    complaint["callback"] = item.get("Item").get("callback").get("S")
    
    key = {"id": {"S": item.get("Item").get("park").get("S")}}
    try:
        park_item = client.get_item(TableName="parks",Key=key)
    except Exception, exception:
        return exception
    park = {}
    park ["id"] = park_item.get("Item").get("id").get("S")
    park ["name"] =  park_item.get("Item").get("name").get("S")
    park ["address"] = park_item.get("Item").get("address").get("S")
    park ["description"] = park_item.get("Item").get("description").get("S")
    park ["image_url"] = park_item.get("Item").get("image_url").get("S")
    park ["location"] = {}
    park ["location"]["lat"] = park_item.get("Item").get("location").get("M").get("lat").get("N")
    park ["location"]["long"] = park_item.get("Item").get("location").get("M").get("long").get("N")
    park ["community"] = get_community(park_item.get("Item").get("community").get("S"), client)
    complaint ["park"] = park

    key = {"id": {"S": item.get("Item").get("user").get("S")}}
    try:
        user_item = client.get_item(TableName="users",Key=key)
    except Exception, exception:
        return exception
    user = {}
    user ["id"] = user_item.get("Item").get("id").get("S")
    user ["name"] =  user_item.get("Item").get("name").get("S")
    user ["image_url"] = user_item.get("Item").get("image_url").get("S")
    user ["phone"] = user_item.get("Item").get("phone").get("S")
    user ["address"] = user_item.get("Item").get("address").get("S")
    user ["email"] = user_item.get("Item").get("address").get("S")
    user ["phone_token"] = user_item.get("Item").get("address").get("S")
    user ["time"] = user_item.get("Item").get("time").get("S")
    user ["location"] = {}
    user ["location"]["lat"] = user_item.get("Item").get("location").get("M").get("lat").get("N")
    user ["location"]["long"] = user_item.get("Item").get("location").get("M").get("long").get("N")
    user ["role"] = get_role(user_item.get("Item").get("role").get("S"),client)
    user ["subscribed_parks"] = get_parks(user_item.get("Item").get("subscribed_parks").get("L"),client)
    user ["supervised_parks"] = get_parks(user_item.get("Item").get("supervised_parks").get("L"),client)

    complaint["user"] = user

    key = {"id": {"S": item.get("Item").get("status").get("S")}}
    status_item = client.get_item(TableName="status", Key=key)
    status = dict()
    status["id"] = status_item["Item"]["id"]["S"]
    status["name"] = status_item["Item"]["name"]["S"]

    complaint["status"] = status

    key = {"id": {"S": item.get("Item").get("priority").get("S")}}
    priority_item = client.get_item(TableName="priorities", Key=key)
    priority = dict()
    priority["id"] = priority_item["Item"]["id"]["S"]
    priority["name"] = priority_item["Item"]["name"]["S"]

    complaint["priority"] = priority

    key = {"id": {"S": item.get("Item").get("category").get("S")}}
    category_item = client.get_item(TableName="categories", Key=key)
    category = dict()
    category["id"] = category_item["Item"]["id"]["S"]
    category["name"] = category_item["Item"]["name"]["S"]

    complaint["category"] = category

    complaint["comments"] = get_comments(item.get("Item").get("comments").get("L"),client)
    
    return complaint