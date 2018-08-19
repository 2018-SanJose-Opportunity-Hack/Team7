""" POST for role.
"""
import uuid
import boto3
import time

def get_boto_list(elements, element_type):
    boto_list = []
    for element in elements:
        boto_list.append({element_type:element})
    return boto_list


def handler(event, context):
    client = boto3.client("dynamodb")
    item = {
            "name": {
                "S": event.get("name")
            },
            "image_url": {
                "S": event.get("image_url")
            },
            "phone": {
                "S": event.get("phone")
            },
            "password": {
                "S": event.get("password")
            },
            "address": {
                "S": event.get("address")
            },
            "email": {
                "S": event.get("email")
            },
            "phone_token": {
                "S": event.get("phone_token")
            },
            "time": {
                "S": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            },
            "role": {
                "S": event.get("role")
            },
            "id": {
                "S": str(uuid.uuid4())
            }
        }
    item ["location"] = {}
    item ["location"]["M"] = {}
    item ["location"]["M"]["lat"] = {"N": str(event.get("location").get("lat"))}
    item ["location"]["M"]["long"] = {"N": str(event.get("location").get("long"))}
    item ["subscribed_parks"] = {"L": get_boto_list(event.get("subscribed_parks"),"S")}
    item ["supervised_parks"] = {"L": get_boto_list(event.get("supervised_parks"),"S")}
    try:
        client.put_item(TableName="users", Item=item)
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event