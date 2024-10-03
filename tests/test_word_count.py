import json
import pytest
import my_lambda

def test_simple_text_count():
    """Tests the word count of a simple text."""
    event = {"body": json.dumps({"0": "Hello World"})}
    expected = {
        "created_by": "Renatex",
        "message": "Word count lambda function",
        "word_count": {"0": 2},
    }

    # Test if return is as expected
    assert my_lambda.word_count(event, None) == expected

def test_no_body():
    """Tests the word count with no body in the request."""
    event = {}
    expected = {
        "created_by": "Renatex",
        "message": "No body in the request"
    }
    assert my_lambda.word_count(event, None) == expected
