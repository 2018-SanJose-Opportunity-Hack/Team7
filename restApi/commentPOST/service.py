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
                "S": event.get("user")
            },
            "complaint": {
                "S": event.get("complaint")
            },
            "id": {
                "S": str(uuid.uuid4())
            }
        }
    try:
        client.put_item(TableName="comments", Item=item)
        client.update_item(TableName="complaints", Key={"id":item.get("complaint")},
                           UpdateExpression="SET #sel = list_append(#sel, :val1)",
                           ExpressionAttributeNames={"#sel": "comments"},
                           ExpressionAttributeValues={":val1":{"L":[item.get("id")]}})
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event