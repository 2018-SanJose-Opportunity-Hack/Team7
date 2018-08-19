""" POST for role.
"""
import uuid
import boto3
import time

def get_complaints(ids, boto_client):
    complaints = []
    for id in ids:
        key = {"id": {"S": id}}
        item = boto_client.get_item(TableName="complaints",Key=key)
        complaint = {}
        complaint["id"] = id
        complaint["name"] = item.get("Item").get("title").get("S")
        complaint["description"] = item.get("Item").get("description").get("S")
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
    try:
        items = client.scan(TableName="parks")
    except Exception, exception:
        return exception
    parks = []
    for item in items.get("Items"):
        park = {}
        park ["id"] = item.get("id").get("S")
        park ["name"] =  item.get("name").get("S")
        park ["address"] = item.get("address").get("S")
        park ["description"] = item.get("description").get("S")
        park ["image_url"] = item.get("image_url").get("S")
        park ["location"] = {}
        park ["location"]["lat"] = item.get("location").get("M").get("lat").get("N")
        park ["location"]["long"] = item.get("location").get("M").get("long").get("N")
        park ["community"] = get_community(item.get("community").get("S"), client)
        # park ["complaints"] = get_complaints(item.get("Item").get("community").get("SS"), client)
        parks.append(park)
    return parks