""" POST for role.
"""
import uuid
import boto3
import time
import subprocess
import smtplib

def send_email(msg, toaddrs, fromaddr = 'contact.parksandrec@gmail.com'):
    username = 'contact.parksandrec@gmail.com'
    password = 'parksandrec'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def send_sms(body, sender='7343047252', receiver='6692924707'):

    curl_cmd = "curl 'https://api.twilio.com/2010-04-01/Accounts/AC2ebde9587e0410118d41dd76174c2051/Messages.json' -X POST \
    --data-urlencode 'To=+1{}' \
    --data-urlencode 'From=+1{}' \
    --data-urlencode 'Body={}' \
    -u AC2ebde9587e0410118d41dd76174c2051:391ee2a219a281a65abdfbdce8cc51cb".format(receiver, sender, body)

    result = subprocess.Popen(curl_cmd, shell=True)
    result.wait()

def handler(event, context):
    client = boto3.client("dynamodb")
    item = {
            "image_url": {
                "S": event.get("image_url")
            },
            "time": {
                "S": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            },
            "last_updated": {
                "S": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
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
                "S": "ab8f4f5b-5182-4237-abe6-09daf4a6a039"
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
        client.update_item(TableName="parks", Key={"id":{"S":event.get("park")}},
                           UpdateExpression="SET #sel = list_append(#sel, :val1)",
                           ExpressionAttributeNames={"#sel": "complaints"},
                           ExpressionAttributeValues={":val1":{"L":[item.get("id")]}})
        send_sms(event.get("title") + " Issue has been Created.")
        key = {"id": {"S": event.get("user")}}
        user_item = client.get_item(TableName="users",Key=key)
        email_id = user_item.get("Item").get("email").get("S")
        send_email(event.get("title") + " Issue has been Created.", email_id)
    except Exception, exception:
        return exception
    event["id"]=item.get("id").get("S")
    return event