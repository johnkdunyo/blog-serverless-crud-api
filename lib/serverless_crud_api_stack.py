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


