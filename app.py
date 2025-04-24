#!/usr/bin/env python3
import os
import json
import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack
from cicd.pipeline_stack import CICDPipelineStack


app = cdk.App()

CDK_ACCOUNT = "839284599071"
CDK_REGION = "us-east-1"

target_env = app.node.try_get_context("env") or "dev"
config_file = f"config/{target_env}.json"

try:
    with open(config_file, 'r') as f:
        env_config = json.load(f)
except FileNotFoundError:
    raise ValueError(f"Archivo de configuración '{config_file}' no encontrado para el entorno '{target_env}'")

# Create the pipeline stack
CICDPipelineStack(app, "MyPipelineStack",
    env=cdk.Environment(account=CDK_ACCOUNT, region=CDK_REGION),
)

InfrastructureStack(app, f"InfrastructureStack-{target_env}",
    env=cdk.Environment(account=CDK_ACCOUNT, region=CDK_REGION),
    env_name=target_env,
    lambda_config=env_config.get('lambda', {}),
    environment_vars=env_config.get('environment_vars', {})
    )

app.synth()
