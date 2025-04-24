from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput,
    CfnParameter,
)
from constructs import Construct

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Environment parameter
        env_param = CfnParameter(
            self, "Environment",
            description="Deployment environment (dev, main)",
            default="dev",
            allowed_values=["dev", "main"]
        )
        
        # Create Lambda function with Flask
        hello_lambda = _lambda.Function(
            self, "HelloWorldFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda/hello_world"),
            handler="app.lambda_handler",
            environment={
                "ENVIRONMENT": env_param.value_as_string
            },
            timeout=Duration.seconds(30),
            memory_size=256,
        )
        
        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, "HelloWorldApi",
            rest_api_name=f"Hello World API - {env_param.value_as_string}",
            description="Simple API Gateway with Lambda and Flask",
            handler=hello_lambda,
            proxy=True,
            deploy_options=apigw.StageOptions(
                stage_name=env_param.value_as_string,
                throttling_rate_limit=100,
                throttling_burst_limit=50,
                logging_level=apigw.MethodLoggingLevel.INFO,
                metrics_enabled=True,
            )
        )
        
        # Output the API URL
        CfnOutput(
            self, "ApiUrl",
            description="API Gateway URL",
            value=api.url
        )
