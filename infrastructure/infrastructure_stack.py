from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput,
)
from constructs import Construct

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment="dev", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Store environment as a fixed value, not as a CloudFormation parameter
        # self.environment = environment
        
        # Create Lambda function with Flask
        hello_lambda = _lambda.Function(
            self, "HelloWorldFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda/hello_world"),
            handler="app.lambda_handler",
            environment={
                "ENVIRONMENT": self.environment
            },
            timeout=Duration.seconds(30),
            memory_size=256,
        )
        
        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, "HelloWorldApi",
            rest_api_name=f"Hello World API - {self.environment}",
            description="Simple API Gateway with Lambda and Flask",
            handler=hello_lambda,
            proxy=True,
            deploy_options=apigw.StageOptions(
                stage_name=self.environment,
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
