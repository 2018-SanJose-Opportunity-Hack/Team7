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
    
    try:
        client.update_item(TableName="complaints",
                           Key={"id":{"S":event.get("id")}},
                           UpdateExpression="SET #o = :o",
                           ExpressionAttributeNames={"#o": "status"},
                           ExpressionAttributeValues=
                           {":o":{"S":event.get("status")}})
        client.update_item(TableName="complaints",
                           Key={"id":{"S":event.get("id")}},
                           UpdateExpression="SET #o = :o",
                           ExpressionAttributeNames={"#o": "priority"},
                           ExpressionAttributeValues=
                           {":o":{"S":event.get("priority")}})
        item = client.get_item(TableName="complaints", Key={"id":{"S":event.get("id")}})
        send_sms(item.get("Item").get("title").get("S") + " Issue has been updated.")
        key = {"id": {"S": item.get("Item").get("user").get("S")}}
        user_item = client.get_item(TableName="users",Key=key)
        email_id = user_item.get("Item").get("email").get("S")
        send_email(item.get("Item").get("title").get("S") + " Issue has been updated.", email_id)
    except Exception, exception:
        return exception
    return item