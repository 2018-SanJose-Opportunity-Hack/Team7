""" POST for role.
"""
import uuid
import boto3
import time

def handler(event, context):
    client = boto3.client("dynamodb")
    
    try:
        client.update_item(TableName="complaints",
                           Key={"id":{"S":event.get("id")}},
                           UpdateExpression="SET #o = :o",
                           ExpressionAttributeNames={"#o": "status"},
                           ExpressionAttributeValues=
                           {":o":{"S":event.get("status")}})
        client.update_item(TableName="complaints",
                           Key={"id":{"S":event.get("id")}},
                           UpdateExpression="SET #o = :o",
                           ExpressionAttributeNames={"#o": "priority"},
                           ExpressionAttributeValues=
                           {":o":{"S":event.get("priority")}})
        item = client.get_item(TableName="complaints", Key={"id":{"S":event.get("id")}})
    except Exception, exception:
        return exception
    return item