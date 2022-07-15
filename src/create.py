import os
import json
import random
import string

import boto3

# create DynamoDB instance: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
dynamodb_client = boto3.client("dynamodb")

# Returns a dictionary of environmental variable as key and their values as value.
TABLE_NAME = os.environ["TABLE_NAME"]
DNS_RECORD = os.environ["DNS_RECORD"]


def handler(event, context):
    # get body from event
    event_body = event.get("body")

    # body validation
    if not event_body:
        return {"statusCode": 400, "body": json.dumps(
            {"error": "body is empty"})
                }
    # deserialization of request body
    request_body = json.loads(event_body)

    # long_url validation
    long_url = request_body.get("long_url")
    if not long_url:
        return {"statusCode": 400, "body": json.dumps(
            {"error": "param long_url required"})
                }

    # generate primary key for DynamoDB table
    url_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    # add a new item to the TABLE_NAME
    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "url_id": {"S": url_id},
            "long_url": {"S": long_url},
        }
    )

    # create short_url
    short_url = DNS_RECORD + url_id

    # return short_url
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "url_id": url_id,
                "short_url": short_url,
            }
        )
    }
