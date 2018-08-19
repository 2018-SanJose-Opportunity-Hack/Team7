""" GET for roles
"""
import boto3
import requests
import json


def find_similarity(text1="This is a good book", text2="Amazing book"):
	url = "https://twinword-text-similarity-v1.p.mashape.com/similarity/"
	payload = "text1={}&text2={}".format(text1, text2)
	headers = {
    			'Content-Type': "application/x-www-form-urlencoded",
    			'X-Mashape-Key': "KaJd5e6lWAmshWITUI7kQC7xYVqnp1y4TYrjsnzCO3uKCAcgZg",
    			'Cache-Control': "no-cache",
    			'Postman-Token': "6518c3d4-6139-47d6-ab01-3fa23082cbec"
      	 	  }
	response = requests.request("POST", url, data=payload, headers=headers)
	return (json.loads(response.text)["similarity"])

def handler(event, context):
    client = boto3.client("dynamodb")
    key = {"id": {"S": event.get("id")}}
    items = client.scan(TableName="complaints")
    response = []
    for item in items.get("Items"):
        return find_similarity(item.get("title").get("S"),event.get("title"))
        if find_similarity(item.get("title").get("S"),event.get("title")) > 0.75 and item.get("park").get("S") == event.get("park") and item.get("category").get("S")==event.get("category"):
            response.append(item)
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