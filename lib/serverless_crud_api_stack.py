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
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler='index.handler',
            code=lambda_.Code.from_asset(os.path.join("./", 'resources/blog')), #path to lamdba functions
            environment={
                'PRIMARY_KEY': 'blogID',
                'DYNAMODB_TABLE_NAME': blog_table.table_name
            },
            bundling={
                'externalModules': ['aws-sdk']
            }
        )


        # add permission for handle to access dynamotable
        blog_table.grant_read_write_data(blogs_handler_function)
        

        # Create the API Gateway
        apigw = apigateway.LambdaRestApi(
            self, 
            rest_api_name="Blog RestAPI",
            handler=blogs_handler_function,
            proxy=False
        )


        # routings
        blog_resource = apigw.root.add_resource('blog')
        blog_resource.add_method("GET") #GET /blog
        blog_resource.add_method("POST") #POST /blog

        single_blog = blog_resource.add_resource('{blogID}')
        single_blog.add_method("GET") #GET /blog/:blogID
        single_blog.add_method("DELETE") #DELETE /blog/:blogID
        single_blog.add_method("PUT") #PUT /blog/:blogID


        




