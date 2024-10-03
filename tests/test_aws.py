import os
import io
import json
import pytest
import boto3
import requests
from dotenv import load_dotenv

@pytest.mark.local
def test_function(verbose: bool = True):
    """
    Test the Lambda function by asserting its existence and expected output.
    """
    load_dotenv()
    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    function_name = os.getenv("FUNCTION_NAME")

    def function_exists(lambda_client, function_name) -> bool:
        """
        Check if the function exists. Return True if it does, False otherwise.
        """
        try:
            lambda_client.get_function(FunctionName=function_name)
            return True
        except lambda_client.exceptions.ResourceNotFoundException:
            return False

    def function_invoke(lambda_client, function_name) -> dict:
        """
        Invoke the function. Return the response payload decoded as a string.
        """
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
        )

        payload = response["Payload"]

        return io.BytesIO(payload.read()).read().decode("utf-8")

    assert function_exists(lambda_client, function_name) is True, f"Function {function_name} does not exist"

    response = function_invoke(lambda_client, function_name)
    response = json.loads(response)
    if verbose:
        print("Lambda function invoked successfully!")
        print("Response:", response)
    assert response["message"] == "No body in the request", "Function did not return the expected message"

@pytest.mark.local
def test_api(verbose: bool = True):
    """
    Test the API Gateway by sending a POST request and asserting the response.
    """
    load_dotenv()
    url = os.getenv("API_GATEWAY_URL")
    payload = {
        "0": "Hello World!",
        "1": "This is a test",
        "2": "API Gateway is cool",
        "3": "Renatex é o brabo"
    }
    response = requests.post(
        url,
        json=payload,
        timeout=5,
    )
    status_code = response.status_code
    response = json.loads(response.text)
    if verbose:
        print("API Gateway invoked successfully!")
        print("Response:", response)
    assert status_code == 200, "Status code is not 200"

    for key, value in payload.items():
        assert key in response["word_count"], f"Key {key} not found in response"
        assert response["word_count"][key] == len(value.split()), f"Word count for key {key} is not correct. Expected {len(value.split())}, got {response['word_count'][key]}"
