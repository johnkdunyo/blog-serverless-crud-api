import os
import aws_cdk
from aws_cdk import (
    # Duration,
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
            table_name="blog_table",
            partition_key=dynamodb.Attribute(
                name="blogId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="dateCreated",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # or PROVISIONED based on your needs
            removal_policy=aws_cdk.RemovalPolicy.DESTROY  # Change to RETAIN if you want to keep the table on stack deletion
        )

        # lamdba handle for the blogs
        blogs_handler_function = lambda_.Function(
            self, id='blogLambdaFunction',
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler='index.handler',
            code=lambda_.Code.from_asset(os.path.join("./", 'resources/blog')), #path to lamdba functions
            environment={
                'PRIMARY_KEY': 'blogID',
                'DYNAMODB_TABLE_NAME': blog_table.table_name
            }
        )


        # add permission for handle to access dynamotable
        blog_table.grant_read_write_data(blogs_handler_function)
        

        # Create the API Gateway
        apigw = apigateway.LambdaRestApi(
            self, 
            id="blogRestAPI",
            rest_api_name="blog_restapi",
            handler=blogs_handler_function,
            proxy=True,
            api_key_source_type= apigateway.ApiKeySourceType.HEADER #added api source key
        )

        # define api key
        api_key = apigateway.ApiKey(self, id="blogApiKey", value="MyNewApiKey0123456789")

        # define usage plan
        usage_plan = apigateway.UsagePlan(self, id="blogApiUsagePlan", name="blog_api_usage_plan", api_stages=[  {
                    'api': apigw,
                    'stage': apigw.deployment_stage,
                },])
        
        usage_plan.add_api_key(api_key)  #add api key to usage plan

        # routings
        blog_resource = apigw.root.add_resource('blog',)
        blog_resource.add_method("GET") #GET /blog
        blog_resource.add_method("POST") #POST /blog

        single_blog = blog_resource.add_resource('{blogID}')
        single_blog.add_method("GET") #GET /blog/:blogID
        single_blog.add_method("DELETE") #DELETE /blog/:blogID
        single_blog.add_method("PUT") #PUT /blog/:blogID


        # output api to consule after deployment
        aws_cdk.CfnOutput(self, 'API Key ID', value=api_key.key_id)

        




