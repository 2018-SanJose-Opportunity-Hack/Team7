""" POST for role.
"""
import uuid
import boto3
import time

def handler(event, context):
    client = boto3.client("dynamodb")
    item = {
            "time": {
                "S": str(time.time())
            },
            "description": {
                "S": event.get("description")
            },
            "user": {
                "S": event.get("user_id")
            },
            "complaint": {
                "S": event.get("complaint_id")
            },
            "id": {
                "S": str(uuid.uuid4())
            }
        }
    try:
        client.put_item(TableName="comments", Item=item)
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event