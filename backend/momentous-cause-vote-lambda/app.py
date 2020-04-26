import os
import boto3
import json
import decimal
from pprint import pprint as pp

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder


def lambda_handler(event, context):
    if event["httpMethod"] == "GET":
        response = get_cause_vote(event, context)
        return response
    if event["httpMethod"] == "POST":
        response = post_cause_vote(event, context)
        return response
    if event["httpMethod"] == "DELETE":
        response = delete_cause_vote(event, context)
        return response


def get_cause_vote(event, context):
    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]
    cause_id = event["pathParameters"]["cause_id"]

    PK, SK = _get_keys(user_id, cause_id)
    print("Key: ", json.dumps({"PK": PK, "SK": SK}, indent=4))

    try:
        data = table.get_item(Key={"PK": PK, "SK": SK}, ReturnConsumedCapacity="TOTAL")
        if not data.get("Item"):
            raise KeyError

    except ClientError as e:
        print(e.response["Error"]["Message"])
        return _response(500, {"status": "DynamoDB Client Error"})
    except KeyError as e:
        print(e)
        return _response(404, {"status": "ITEM NOT FOUND"})
    else:
        print("GetItem succeeded:")
        print(json.dumps(data, indent=4, cls=DecimalEncoder))

    return _response(200, data["Item"])


def post_cause_vote(event, context):
    import uuid

    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]
    cause_id = event["pathParameters"]["cause_id"]

    payload = json.loads(event["body"])
    vote = payload["vote"]
    PK, SK = _get_keys(user_id, cause_id)
    print("Key: ", json.dumps({"PK": PK, "SK": SK}, indent=4))
    item = dict(payload)
    item.update(
        {
            "PK": PK,
            "SK": SK,
            "user_id": user_id,
            "cause_id": cause_id,
            "vote_created_at": _date_time_now(),
        }
    )

    try:
        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(SK)",
            ReturnConsumedCapacity="TOTAL",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return _response(409, {"status": "Item already exists"})
        print(e.response["Error"]["Message"])
        return _response(500, {"status": "DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        PK, SK = _get_cause_keys(user_id, cause_id)
        if item["vote"] == "UP":
            vote_attribute = "cause_total_up_votes"
        else:
            vote_attribute = "cause_total_down_votes"
        response = table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression="SET #vote = #vote + :vote",
            ConditionExpression="attribute_exists(SK)",
            ExpressionAttributeNames={"#vote": vote_attribute},
            ExpressionAttributeValues={":vote": 1},
            ReturnValues="ALL_NEW",
            ReturnConsumedCapacity="TOTAL",
        )
    return _response(201, response["Attributes"])


def delete_cause_vote(event, context):

    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]
    cause_id = event["pathParameters"]["cause_id"]

    # payload = json.loads(event["body"])
    # vote = payload["vote"]
    PK, SK = _get_keys(user_id, cause_id)
    # item = dict(payload)
    # item.update({"PK": PK, "SK": SK})

    try:
        response = table.delete_item(
            Key={"PK": PK, "SK": SK},
            ConditionExpression="attribute_exists(SK)",
            ReturnConsumedCapacity="TOTAL",
            ReturnValues="ALL_OLD",
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return _response(404, {"status": "ITEM NOT FOUND"})

        print(e.response["Error"]["Message"])
        return _response(500, {"status": "DynamoDB Client Error"})
    else:
        print("DeleteItem succeeded:")
        PK, SK = _get_cause_keys(user_id, cause_id)
        if response["Attributes"]["vote"] == "UP":
            vote_attribute = "cause_total_up_votes"
        else:
            vote_attribute = "cause_total_down_votes"
        response = table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression="SET #vote = #vote - :vote",
            ConditionExpression="attribute_exists(SK)",
            ExpressionAttributeNames={"#vote": vote_attribute},
            ExpressionAttributeValues={":vote": 1},
            ReturnValues="ALL_NEW",
            ReturnConsumedCapacity="TOTAL",
        )
    print("Item delete response: ", response)

    return _response(200, response["Attributes"])


def _get_keys(user_id, cause_id):
    pk = "MOMENTOUS#cause#vote"
    sk = "CAUSE#" + cause_id + "#USER#" + user_id
    return (
        pk,
        sk,
    )


def _get_cause_keys(user_id, cause_id):
    pk = "MOMENTOUS#cause"
    sk = "USER#" + user_id + "#CAUSE#" + cause_id
    return (
        pk,
        sk,
    )


def _response(status_code, json_body):
    body = json.dumps(json_body, cls=DecimalEncoder)

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": body,
    }


def _date_time_now():
    import datetime

    return str(datetime.datetime.utcnow().replace(microsecond=0).isoformat("T")) + "Z"


def __get_table_client():
    TABLE_NAME = os.getenv("TABLE_NAME")
    # AWS_REGION_DYNAMODB = os.getenv("AWS_REGION_DYNAMODB")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    return table
