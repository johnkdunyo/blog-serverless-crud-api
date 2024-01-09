from aws_cdk import (
    # Duration,
    core,
    Stack,
    aws_dynamodb as dynamodb
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
            self,"blogTable",
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

