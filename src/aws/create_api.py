import os
import boto3
import random
import string
from dotenv import load_dotenv

def main():
    load_dotenv()

    lambda_function_name = "sayHello_renatex" # Example: sayHello_<INSPER_USERNAME>
    api_gateway_name = "api_hello_renatex" # Example: api_hello_<INSPER_USERNAME>"

    id_num = "".join(random.choices(string.digits, k=7))

    api_gateway = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_function = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_function_get = lambda_function.get_function(FunctionName=lambda_function_name)

    print(lambda_function_get)

    api_gateway_create = api_gateway.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey="ANY /", # Here you can change to GET POST and provide route like "GET /hello"
        Target=lambda_function_get["Configuration"]["FunctionArn"],
    )

    api_gateway_permissions = lambda_function.add_permission(
        FunctionName=lambda_function_name,
        StatementId="api-gateway-permission-statement-" + id_num,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
    )

    print("API Endpoint:", api_gateway_create["ApiEndpoint"])

if __name__ == "__main__":
    main()