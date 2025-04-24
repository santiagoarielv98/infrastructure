from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput,
)
from constructs import Construct

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,env_name: str, lambda_config: dict, 
                 environment_vars: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        memory_size = lambda_config.get('memory_size', 128)
        timeout = lambda_config.get('timeout', 30)

        if 'ENVIRONMENT' not in environment_vars:
            environment_vars['ENVIRONMENT'] = env_name

        # Create Lambda function
        hello_lambda = _lambda.Function(
            self, 
            f"HelloWorldFunction-{env_name}",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset("lambda/hello_world"),
            memory_size=memory_size,
            timeout=Duration.seconds(timeout),
            environment=environment_vars
        )
        
        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, 
            "HelloWorldApi",
            handler=hello_lambda,
            rest_api_name=f"HelloApi",
        )
