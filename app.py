#!/usr/bin/env python3
import os
import json
import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack


app = cdk.App()

target_env = app.node.try_get_context("env") or "dev"
config_file = f"config/{target_env}.json"

try:
    with open(config_file, 'r') as f:
        env_config = json.load(f)
except FileNotFoundError:
    raise ValueError(f"Archivo de configuración '{config_file}' no encontrado para el entorno '{target_env}'")

InfrastructureStack(app, f"InfrastructureStack-{target_env}",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account='839284599071', region='us-east-1'),
    env_name=target_env,
    lambda_config=env_config.get('lambda', {}),
    environment_vars=env_config.get('environment_vars', {})

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
