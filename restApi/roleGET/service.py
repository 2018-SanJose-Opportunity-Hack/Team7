""" GET for roles
"""
import boto3


def handler(event, context):
    client = boto3.client("dynamodb")
    key = {"id": {"S": event.get("id")}}
    item = client.get_item(TableName="roles", Key=key)
    response = dict()
    response["id"] = item["Item"]["id"]["S"]
    response["name"] = item["Item"]["name"]["S"]
    return response



""" body mapping templates: 
input:
{"id":"$input.params('id')"}
output:
#set($inputRoot = $input.path('$'))
{
    "id": "$inputRoot.id",
    "name": "$inputRoot.name"
}
"""