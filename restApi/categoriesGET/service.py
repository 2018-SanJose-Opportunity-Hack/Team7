""" POST for role.
"""
import uuid
import boto3 

def handler(event, context):
    client = boto3.client("dynamodb")
    try:
        items = client.scan(TableName="categories")
    except Exception, exception:
        return exception
    categories = []
    for item in items.get("Items"):
        category = {}
        category ["id"] = item.get("id").get("S")
        category ["name"] =  item.get("name").get("S")
        categories.append(category)
    return categories