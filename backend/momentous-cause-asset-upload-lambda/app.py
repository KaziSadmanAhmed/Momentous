import os
import json
import boto3
import base64
import uuid
from cgi import parse_header, parse_multipart
from io import BytesIO

client = boto3.client("s3")


def upload_file(bucketName, directory_name, file_name, file_content):
    response = client.list_objects_v2(Bucket=bucketName, Prefix=directory_name)
    if response.get("Contents"):
        try:
            s3_response = client.put_object(
                Bucket=bucketName,
                Key=directory_name + file_name,
                ACL="public-read",
                Body=file_content,
            )
        except Exception as e:
            raise IOError(e)
        return (
            "https://momentous.cloud" + directory_name.replace("webapp", "") + file_name
        )
    else:
        client.put_object(Bucket=bucketName, Key=(directory_name))
        try:
            s3_response = client.put_object(
                Bucket=bucketName,
                Key=directory_name + file_name,
                ACL="public-read",
                Body=file_content,
            )
        except Exception as e:
            raise IOError(e)
        return (
            "https://momentous.cloud" + directory_name.replace("webapp", "") + file_name
        )


def lambda_handler(event, context):
    # print(json.dumps(event))
    directory_name = "webapp/assets/" + event["pathParameters"]["user_id"] + "/"
    bucket = "momentous.cloud"
    file_name = str(uuid.uuid4()) + ".png"

    # body = event["body"]
    # print(body.keys())
    # print(event["headers"]["Content-Type"])
    # file_content = body[body.find(",") + 1 :]

    # if event["isBase64Encoded"] == "true":
    #     file_content = base64.b64decode(file_content + "===")

    # print(file_content)
    content_type = event["headers"].get("Content-Type") or event["headers"].get(
        "content-type"
    )
    c_type, p_dict = parse_header(content_type)
    assert c_type == "multipart/form-data"
    p_dict["boundary"] = bytes(p_dict["boundary"], "utf-8")

    content_length = (
        event["headers"].get("Content-Length")
        or event["headers"].get("content-length")
        or event["headers"].get("Image-Size")
        or event["headers"].get("image-size")
    )
    p_dict["CONTENT-LENGTH"] = int(content_length)
    decoded_string = base64.b64decode(event["body"])
    form_data = parse_multipart(BytesIO(decoded_string), p_dict)

    # print(len(form_data["image"]))

    response = upload_file(bucket, directory_name, file_name, form_data["image"][0])

    return {
        "statusCode": 200,
        "body": json.dumps({"image_url": response}),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }
