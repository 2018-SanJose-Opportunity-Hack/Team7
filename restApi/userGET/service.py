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
    key = {"id": {"S": event.get("id")}}
    try:
        item = client.get_item(TableName="users",Key=key)
    except Exception, exception:
        return exception
    user = {}
    user ["id"] = item.get("Item").get("id").get("S")
    user ["name"] =  item.get("Item").get("name").get("S")
    user ["image_url"] = item.get("Item").get("image_url").get("S")
    user ["phone"] = item.get("Item").get("phone").get("S")
    user ["address"] = item.get("Item").get("address").get("S")
    user ["email"] = item.get("Item").get("address").get("S")
    user ["phone_token"] = item.get("Item").get("address").get("S")
    user ["time"] = item.get("Item").get("time").get("S")
    user ["location"] = {}
    user ["location"]["lat"] = item.get("Item").get("location").get("M").get("lat").get("N")
    user ["location"]["long"] = item.get("Item").get("location").get("M").get("long").get("N")
    user ["role"] = get_role(item.get("Item").get("role").get("S"),client)
    user ["subscribed_parks"] = get_parks(item.get("Item").get("subscribed_parks").get("L"),client)
    user ["supervised_parks"] = get_parks(item.get("Item").get("supervised_parks").get("L"),client)
    # park ["complaints"] = get_complaints(item.get("Item").get("community").get("SS"), client)
    return user