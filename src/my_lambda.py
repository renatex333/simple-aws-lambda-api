"""
Module to define lambda functions that will be deployed to AWS Lambda.

Functions:
- say_hello: Handler function that returns a message.
- word_count: Handler function that counts the number of words in phrases.

Author: Renatex
"""

import json

def say_hello(event, context):
    """
    This is a simple lambda function that returns a message.
    Also called the handler function.
    """
    return {
        "created_by": "Renatex",
        "message": "Hello World!"
    }

def word_count(event, context):
    """
    Handler for word count lambda function
    """
    if "body" not in event:
        return {
            "created_by": "Renatex",
            "message": "No body in the request"
        }

    body = json.loads(event["body"])
    word_counter = dict()
    for key, value in body.items():
        word_counter[key] = len(value.split())

    return {
        "created_by": "Renatex",
        "message": "Word count lambda function",
        "word_count": word_counter,
    }
