""" POST for role.
"""
import uuid
import boto3

def handler(event, context):
    client = boto3.client("dynamodb")
    item = {
            "name": {
                "S": event.get("name")
            },
            "id": {
                "S": str(uuid.uuid4())
            }
        }
    try:
        client.put_item(TableName="roles", Item=item)
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event