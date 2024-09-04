"""
AWS Lambda Function Tutorial to invoke a Lambda function in your AWS account
"""

import os
import io
import boto3
from dotenv import load_dotenv


def main():
    load_dotenv()

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Lambda function name
    # Provide function name: sayHello_<YOUR_INSPER_USERNAME>
    function_name = "sayHello_renatex"

    try:
        # Invoke the function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
        )

        payload = response["Payload"]

        txt = io.BytesIO(payload.read()).read().decode("utf-8")
        print(f"Response:\n{txt}")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
