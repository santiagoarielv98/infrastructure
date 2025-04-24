import os
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    environment = os.environ.get('ENVIRONMENT', 'dev')
    return jsonify({
        'message': f'Hello from {environment} environment!',
        'status': 'success'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy'
    })

def lambda_handler(event, context):
    """
    Lambda function handler that processes API Gateway events using Flask
    """
    # Get HTTP method and path from the event
    http_method = event['httpMethod']
    path = event['path']
    
    # Create WSGI environment
    environ = {
        'REQUEST_METHOD': http_method,
        'PATH_INFO': path,
        'QUERY_STRING': event.get('queryStringParameters', '') or '',
        'CONTENT_LENGTH': str(len(event.get('body', '') or '')),
        'CONTENT_TYPE': event.get('headers', {}).get('Content-Type', ''),
        'wsgi.version': (1, 0),
        'wsgi.input': None,
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': 'lambda',
        'SERVER_PORT': '443',
    }

    # Process the request with Flask
    with app.request_context(environ):
        try:
            # Handle the request and get the response
            response = app.full_dispatch_request()
            
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            } 