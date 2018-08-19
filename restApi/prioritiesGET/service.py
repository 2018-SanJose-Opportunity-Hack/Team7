""" POST for role.
"""
import uuid
import boto3 

def handler(event, context):
    client = boto3.client("dynamodb")
    try:
        items = client.scan(TableName="priorities")
    except Exception, exception:
        return exception
    priorities = []
    for item in items.get("Items"):
        priority = {}
        priority ["id"] = item.get("id").get("S")
        priority ["name"] =  item.get("name").get("S")
        priorities.append(priority)
    return priorities