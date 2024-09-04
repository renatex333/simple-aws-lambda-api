"""
Script to create a simple API using AWS Lambda and API Gateway
"""

import os
import sys
import boto3
import random
import string
from dotenv import load_dotenv, set_key

def main(update=False):
    load_dotenv()

    lambda_function_name = "word_count_renatex"
    api_gateway_name = "api_word_count_renatex"

    data_dir = os.path.relpath("data", os.getcwd())
    zip_file = "my_lambda.zip"
    handler = "my_lambda.word_count" # Python file DOT handler function
    zip_file_path = os.path.join(data_dir, zip_file)
    lambda_function_arn = create_function(lambda_function_name, zip_file_path, handler, update)
    create_api(api_gateway_name, lambda_function_arn, update)
    

def create_function(lambda_function_name, zip_file_path, handler, update) -> str:
    """
    Create a new Lambda function using the provided ZIP file
    """
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

    # Read the contents of the zip file to deploy
    with open(zip_file_path, "rb") as f:
        zip_to_deploy = f.read()

    if update:
        try:
            lambda_client.delete_function(FunctionName=lambda_function_name)
            print("Function Deleted!")
        except Exception as e:
            print("Error deleting function:", e)
    lambda_response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime="python3.9",
        Role=lambda_role_arn,
        Handler=handler,
        Code={"ZipFile": zip_to_deploy},
    )

    id_num = "".join(random.choices(string.digits, k=7))
    api_gateway_permissions = lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId="api-gateway-permission-statement-" + id_num,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
    )

    try:
        print("Function Created!")
        print("Function ARN:", lambda_response["FunctionArn"])
    except KeyError as e:
        raise Exception("Error creating function:", e)
    
    return lambda_response["FunctionArn"]
    
def create_api(api_gateway_name, lambda_function_arn, update):
    """
    Create a new API Gateway with a route to the provided Lambda function
    """
    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    if update:
        try:
            api_gateway_client.delete_api(ApiId=os.getenv("API_GATEWAY_ID"))
            print("API Gateway Deleted!")
        except Exception as e:
            print("Error deleting API Gateway:", e)
    api_route = "/word-count"
    api_gateway_create = api_gateway_client.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}", # Here you can change to GET POST and provide route like "GET /hello"
        Target=lambda_function_arn,
    )

    try:
        print("API Gateway Created!")
        print("API Endpoint:", api_gateway_create["ApiEndpoint"] + api_route)
        set_key(".env", "API_GATEWAY_ID", api_gateway_create["ApiId"])
        set_key(".env", "API_GATEWAY_URL", api_gateway_create["ApiEndpoint"] + api_route)
    except KeyError as e:
        raise Exception("Error creating API Gateway:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        main(update=True)
    else:
        main()