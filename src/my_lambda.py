import json

"""
This is a simple lambda function that returns a message.
Also called the handler function.
"""
def say_hello(event, context):
    return {
        "created_by": "Renatex",
        "message": "Hello World!"
    }

"""
Handler for word count lambda function
"""
def word_count(event, context):
    if "body" not in event:
        return {
            "created_by": "Renatex",
            "message": "No body in the request"
        }
    
    body = json.loads(event["body"])
    word_count = dict()
    for key, value in body.items():
        word_count[key] = len(value.split())

    return {
        "created_by": "Renatex",
        "message": "Word count lambda function",
        "word_count": word_count,
    }