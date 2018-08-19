""" POST for role.
"""
import uuid
import boto3
import time

def get_complaints(ids, boto_client):
    complaints = []
    for id in ids:
        key = {"id": id}
        item = boto_client.get_item(TableName="complaints",Key=key)
        complaint = {}
        complaint["id"] = id
        complaint["title"] = item.get("Item").get("title").get("S")
        complaint["description"] = item.get("Item").get("description").get("S")
        complaint["time"] = item.get("Item").get("time").get("S")
        
        key = {"id": {"S": item.get("Item").get("user").get("S")}}
        try:
            user_item = boto_client.get_item(TableName="users",Key=key)
        except Exception, exception:
            return exception
        user = {}
        user ["id"] = user_item.get("Item").get("id").get("S")
        user ["name"] =  user_item.get("Item").get("name").get("S")
        user ["image_url"] = user_item.get("Item").get("image_url").get("S")

        complaint["user"] = user

        complaints.append(complaint)
    return complaints

def get_community(id, boto_client):
    key = {"id": {"S": id}}
    item = boto_client.get_item(TableName="communities",Key=key)
    community = {}
    community["id"] = id
    community["name"] = item.get("Item").get("name").get("S")
    return community    

def handler(event, context):
    client = boto3.client("dynamodb")
    key = {"id": {"S": event.get("id")}}
    try:
        item = client.get_item(TableName="parks",Key=key)
    except Exception, exception:
        return exception
    park = {}
    park ["id"] = item.get("Item").get("id").get("S")
    park ["name"] =  item.get("Item").get("name").get("S")
    park ["address"] = item.get("Item").get("address").get("S")
    park ["description"] = item.get("Item").get("description").get("S")
    park ["image_url"] = item.get("Item").get("image_url").get("S")
    park ["location"] = {}
    park ["location"]["lat"] = item.get("Item").get("location").get("M").get("lat").get("N")
    park ["location"]["long"] = item.get("Item").get("location").get("M").get("long").get("N")
    park ["community"] = get_community(item.get("Item").get("community").get("S"), client)
    park ["complaints"] = get_complaints(item.get("Item").get("complaints").get("L"), client)
    return park