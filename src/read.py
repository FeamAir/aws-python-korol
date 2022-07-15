import os
import json

import boto3


# create DynamoDB instance: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
dynamodb_client = boto3.client("dynamodb")

# Returns a dictionary of environmental variable as key and their values as value.
TABLE_NAME = os.environ["TABLE_NAME"]


def handler(event, context):

    # take url_id from event
    url_id = event["pathParameters"]["url_id"]

    # get an item from TABLE_NAME
    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"url_id": {"S": url_id}}).get("Item")

    # result validation
    if not result:
        return {"statusCode": 404, "body": json.dumps(
            {"error": "Url not found"})
                }

    # get long_url from result
    long_url = result.get("long_url").get("S")

    # make redirect to long_url
    response = {
        "headers": {"Location": long_url},
        "statusCode": 301,
    }

    return response
