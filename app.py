#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack

app = cdk.App()

# Obtener el entorno del contexto o usar 'dev' por defecto
env_name = app.node.try_get_context("env") or "dev"

# Validar que el entorno sea válido
if env_name not in ["dev", "prod"]:
    raise ValueError(f"El entorno '{env_name}' no es válido. Use 'dev' o 'prod'.")

InfrastructureStack(
    app, 
    f"InfrastructureStack-{env_name}",
    environment=env_name,
    # Especificar la cuenta/región AWS para el despliegue
    env=cdk.Environment(
        account='839284599071', 
        region='us-east-1'
    ),
    description=f"Infraestructura para APIs de ejemplo - Entorno: {env_name}"
)

app.synth()
