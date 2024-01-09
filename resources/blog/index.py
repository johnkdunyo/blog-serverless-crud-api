import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")


def handler(event, context):
    logger.info(event, context)
    message = "Test Success"
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }