import os
import io
import json
import boto3
import requests
from dotenv import load_dotenv

def test_function(lambda_client, function_name):

    assert function_exists(lambda_client, function_name) == True, f"Function {function_name} does not exist"

    response = function_invoke(lambda_client, function_name)
    response = json.loads(response)
    print(response)
    assert response["message"] == "No body in the request", "Function did not return the expected message"
    

def function_exists(lambda_client, function_name) -> bool:
    """
    Check if the function exists
    """
    try:
        lambda_client.get_function(FunctionName=function_name)
        return True
    except lambda_client.exceptions.ResourceNotFoundException:
        return False
    
def function_invoke(lambda_client, function_name) -> dict:
    """
    Invoke the function
    """
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
    )

    payload = response["Payload"]

    return io.BytesIO(payload.read()).read().decode("utf-8")

def test_api():
    url = os.getenv("API_GATEWAY_URL")
    response = requests.post(url, json={"0": "Hello World!", "1": "This is a test", "2": "API Gateway", "3": "Renatex é o brabo"})
    status_code = response.status_code
    response = json.loads(response.text)
    print(response)
    assert status_code == 200, "Status code is not 200"
    assert response["word_count"]["0"] == 2, "Word count for 'Hello World!' is not 2"
    assert response["word_count"]["1"] == 4, "Word count for 'This is a test' is not 4"
    assert response["word_count"]["2"] == 2, "Word count for 'API Gateway' is not 2"
    assert response["word_count"]["3"] == 4, "Word count for 'Renatex é o brabo' is not 4"

if __name__ == "__main__":
    load_dotenv()

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    test_function(lambda_client, "word_count_renatex")
    test_api()