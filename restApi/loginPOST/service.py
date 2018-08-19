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


def handler(event, context):
    client = boto3.client("dynamodb")
    try:
        users = client.scan(TableName="users")
    except Exception, exception:
        return exception
    for user in users.get("Items"):
        if user.get("email").get("S") == event.get("email") and user.get("password").get("S") == event.get("password"):
            auth_user = {}
            auth_user ["id"] = user.get("id").get("S")
            auth_user ["name"] =  user.get("name").get("S")
            auth_user ["image_url"] = user.get("image_url").get("S")
            auth_user ["phone"] = user.get("phone").get("S")
            auth_user ["address"] = user.get("address").get("S")
            auth_user ["email"] = user.get("address").get("S")
            auth_user ["phone_token"] = user.get("address").get("S")
            auth_user ["time"] = user.get("time").get("S")
            auth_user ["location"] = {}
            auth_user ["location"]["lat"] = user.get("location").get("M").get("lat").get("N")
            auth_user ["location"]["long"] = user.get("location").get("M").get("long").get("N")
            auth_user ["role"] = get_role(user.get("role").get("S"),client)
            auth_user ["subscribed_parks"] = get_parks(user.get("subscribed_parks").get("L"),client)
            auth_user ["supervised_parks"] = get_parks(user.get("supervised_parks").get("L"),client)
            return auth_user
    raise Exception("Incorrect username and/or password")