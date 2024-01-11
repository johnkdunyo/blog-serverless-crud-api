import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")
table_name = 'blog_table'


# table = dynamodb.Table("blog_table")


def handler(event, context):
    logger.info(event)
    route_key = f"{event['httpMethod']} {event['resource']}"
    print(route_key)

    # Set default response, override with data from DynamoDB if any
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
    }
    response_body = {"message": "Unsupported Route"}

    try:
        # add a blog
        if route_key == "POST /blog":
            # validate request body
            blog_data = json.loads(event["body"])
            logger.info(blog_data)
            if not blog_data:
                # blog data does not exists
                status_code = 404
                response_body["message"] = 'Please provide a valid blog data'

            response = dynamodb.put_item(
                TableName=table_name,
                Item={
                    'blogId': {'S': str(uuid.uuid4())},
                    'title': {'S': blog_data['title']},
                    'description': {'S': blog_data['description']},
                    'author': {'S': blog_data['author']},
                    'dateCreated': {'S': datetime.utcnow().isoformat()}
                }
            )
            status_code = 202
            response_body['message'] = 'Data inserted successfully'
            response_body["blog"] = response

        # get all blogs
        if route_key == "GET /blog":
            response = dynamodb.scan(TableName=table_name)
            logger.info(response['Items'])
            status_code = 200
            response_body["message"] = "Blogs retrieved successfully"
            response_body["blogs"] = response["Items"]

    except Exception as err:
        response_body = {'Error:': str(err)}
        logger.error(str(err))

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(response_body)
    }
