""" POST for role.
"""
import uuid
import boto3
import time

def handler(event, context):
    client = boto3.client("dynamodb")
    item = {
            "image_url": {
                "S": event.get("image_url")
            },
            "time": {
                "S": str(time.time())
            },
            "last_updated": {
                "S": str(time.time())
            },
            "description": {
                "S": event.get("description")
            },
            "callback": {
                "S": event.get("callback")
            },
            "title": {
                "S": event.get("title")
            },
            "park": {
                "S": event.get("park")
            },
            "user": {
                "S": event.get("user")
            },
            "category": {
                "S": event.get("category")
            },
            "priority": {
                "S": event.get("priority")
            },
            "status": {
                "S": "89cf74ae-5c72-4ef4-9548-99bb73c4f760"
            },
            "id": {
                "S": str(uuid.uuid4())
            }
        }
    item ["comments"] = {"L": []}
    try:
        client.put_item(TableName="complaints", Item=item)
        client.update_item(TableName="parks", Key={"id":event.get("park")},
                           UpdateExpression="SET #sel = list_append(#sel, :val1)",
                           ExpressionAttributeNames={"#sel": "complaints"},
                           ExpressionAttributeValues={":val1":{"L":[item.get("id").get("S")]}})
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event