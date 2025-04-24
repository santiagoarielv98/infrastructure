import json
import os

def lambda_handler(event, context):
    """
    Simple Lambda function that returns a greeting message.
    
    Parameters:
    event (dict): API Gateway event data
    context (obj): Runtime information
    
    Returns:
    dict: API Gateway response with status code and body
    """
    # Get environment variables
    environment = os.environ.get('ENVIRONMENT', 'unknown')
    print(f"Environment: {environment}")
    
    # Process the event
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    
    # Create response message
    message = f"Hello from Lambda! You made a {method} request to {path}"
    
    # Log information
    print(f"Request processed in {environment} environment")
    print(f"Event: {json.dumps(event)}")
    
    # Return response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": message,
            "environment": environment,
            "timestamp": context.get_remaining_time_in_millis()
        })
    }