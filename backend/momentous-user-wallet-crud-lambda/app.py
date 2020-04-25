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
        response = get_user_wallet_details(event, context)
        return response
    if event["httpMethod"] == "POST":
        response = post_user_wallet_details(event, context)
        return response
    if event["httpMethod"] == "PUT":
        response = put_user_wallet_details(event, context)
        return response


def get_user_wallet_details(event, context):

    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]

    PK, SK = _get_keys(user_id)
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


def post_user_wallet_details(event, context):
    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]

    payload = json.loads(event["body"])
    PK, SK = _get_keys(user_id)
    print("Key: ", json.dumps({"PK": PK, "SK": SK}, indent=4))
    item = dict(payload)
    # hash_generated_total = int(item["hash_generated_daily"]) + int(item["hash_balance"])
    item.update(
        {
            "PK": PK,
            "SK": SK,
            "user_id": user_id,
            "hash_generated_total": 0,
            "hash_generated_daily": 0,
            "hash_balance": 0,
            "wallet_created_at": _date_time_now(),
            "wallet_updated_at": _date_time_now(),
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
    return _response(201, item)


def put_user_wallet_details(event, context):

    table = __get_table_client()
    user_id = event["pathParameters"]["user_id"]

    payload = json.loads(event["body"])
    PK, SK = _get_keys(user_id)
    # item = dict(payload)
    # item.update({"PK": PK, "SK": SK})

    try:
        response = table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression="SET #hash_generated_daily = #hash_generated_daily + :hash_increment, #hash_generated_total = #hash_generated_total + :hash_increment, #wallet_updated_at = :wallet_updated_at",
            ConditionExpression="attribute_exists(SK)",
            ExpressionAttributeNames={
                "#hash_generated_total": "hash_generated_total",
                "#hash_generated_daily": "hash_generated_daily",
                "#wallet_updated_at": "wallet_updated_at",
            },
            ExpressionAttributeValues={
                ":hash_increment": int(payload["hash_increment"]),
                ":wallet_updated_at": _date_time_now(),
            },
            ReturnValues="ALL_NEW",
            ReturnConsumedCapacity="TOTAL",
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return _response(404, {"status": "ITEM NOT FOUND"})

        print(e.response["Error"]["Message"])
        return _response(500, {"status": "DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        # print(json.dumps(table_record, indent=4, cls=DecimalEncoder))
    print("Item update response: ", response)
    if not response.get("Attributes"):
        return _response(404, {"status": "ITEM NOT FOUND"})
    return _response(200, response["Attributes"])


def _get_keys(user_id):
    pk = "MOMENTOUS#user"
    sk = "WALLET#USER#" + user_id
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
