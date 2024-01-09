import os
from aws_cdk import (
    # Duration,
    core,
    Stack,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    # aws_sqs as sqs,
)
from constructs import Construct

class ServerlessCrudApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Define the DynamoDB table
        # blog: PK = blogID, SK = dateCreated, otherFields = body, ImageURL
        blog_table = dynamodb.Table(
            self,
            id="blogTable",
            table_name="Blog Table",
            partition_key=dynamodb.Attribute(
                name="blogId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="dateCreated",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED based on your needs
            removal_policy=core.RemovalPolicy.DESTROY  # Change to RETAIN if you want to keep the table on stack deletion
        )

        # lamdba handle for the blogs
        blogs_handler_function = lambda_.Function(
            self, 'ProductLambdaFunction',
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler='index.handler',
            code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), '/../resources/blog')), #path to lamdba functions
            environment={
                'PRIMARY_KEY': 'id',
                'DYNAMODB_TABLE_NAME': blog_table.table_name
            },
            bundling={
                'externalModules': ['aws-sdk']
            }
        )

       
        # Create the API Gateway
        apigw = apigateway.LambdaRestApi(
            self, 
            rest_api_name="Blog RestAPI",
            handler=blogs_handler_function,
            proxy=False
        )


        




