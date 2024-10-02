"""
Script to:

- Create a new Lambda function from a ZIP file
- Create a new API Gateway to expose the Lambda function

Author: Renatex
"""

import os
import sys
import boto3
import random
import string
import botocore
from dotenv import load_dotenv, set_key, unset_key

def main(zip_file_path: str, handler: str, update: bool = False):
    """
    Create a new Lambda function and API Gateway

    Args:
    - zip_file_path: Path to the ZIP file containing the Lambda function code
    - handler: Handler function for the Lambda function
    - update: Whether to update an existing Lambda function
    """
    load_dotenv()

    lambda_function_name = os.getenv("FUNCTION_NAME")
    api_gateway_name = os.getenv("API_GATEWAY_NAME")

    create_function(lambda_function_name, zip_file_path, handler, update)
    create_api(api_gateway_name, update)

def create_function(
        lambda_function_name: str,
        zip_file_path: str,
        handler: str,
        update: bool
    ) -> str:
    """
    Create a new Lambda function using the provided ZIP file

    Args:
    - lambda_function_name: Name of the Lambda function
    - zip_file_path: Path to the ZIP file containing the Lambda function code
    - handler: Handler function for the Lambda function
    - update: Whether to update an existing Lambda function

    Returns:
    - The ARN of the new Lambda function
    """
    load_dotenv()
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
            print("Existing Function was Deleted!")
            unset_key(".env", "FUNCTION_ARN")
        except (lambda_client.exceptions.ResourceNotFoundException, botocore.exceptions.ParamValidationError):
            print("No existing function found.")

    response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime="python3.9",
        Role=lambda_role_arn,
        Handler=handler,
        Code={"ZipFile": zip_to_deploy},
    )
    function_arn = response["FunctionArn"]
    id_num = "".join(random.choices(string.digits, k=7))
    add_permission_response = lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId="api-gateway-permission-statement-" + id_num,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
    )

    print("Function Created!")
    print(f"Function {lambda_function_name} created with ARN:", function_arn)
    set_key(".env", "\nFUNCTION_ARN", function_arn)

def create_api(api_gateway_name: str, update: bool):
    """
    Create a new API Gateway with a route to the provided Lambda function

    Args:
    - api_gateway_name: Name of the API Gateway
    - update: Whether to update an existing API Gateway
    """
    load_dotenv()
    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    if update:
        api_gateway_id = os.getenv("API_GATEWAY_ID")
        try:
            api_gateway_client.delete_api(ApiId=api_gateway_id)
            print("API Gateway Deleted!")
            unset_key(".env", "API_GATEWAY_ID")
        except (api_gateway_client.exceptions.NotFoundException, botocore.exceptions.ParamValidationError):
            print(f"No existing API Gateway found with ID {api_gateway_id}.")

    lambda_function_arn = os.getenv("FUNCTION_ARN")
    api_route = "/word-count"
    response = api_gateway_client.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}", # Here you can change to GET POST and provide route like "GET /hello"
        Target=lambda_function_arn,
    )

    api_gateway_id = response["ApiId"]
    api_gateway_endpoint = response["ApiEndpoint"] + api_route
    print("API Gateway Created at:", api_gateway_endpoint, "with ID:", api_gateway_id)
    set_key(".env", "API_GATEWAY_ID", api_gateway_id)
    set_key(".env", "API_GATEWAY_URL", api_gateway_endpoint)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <path to zip file> <handler> [update]")
        sys.exit(1)
    ZIP_FILE = sys.argv[1]
    HANDLER = ZIP_FILE.split("/")[-1].replace(".zip", f".{sys.argv[2]}")
    if len(sys.argv) == 4 and sys.argv[-1] == "update":
        print("Updating existing resources...")
        main(zip_file_path=ZIP_FILE, handler=HANDLER, update=True)
    else:
        main(zip_file_path=ZIP_FILE, handler=HANDLER)
