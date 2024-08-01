from src.app.schemas import request

def create_valid_timer_request() -> dict:
    """
    Creating the request body for /timer api
    :return: request body in dict
    """
    _request = {"hours": 1,
        "minutes": 1,
        "seconds": 1,
        "url": "https://www.google.com"
    }
    return _request


def create_invalid_url_timer_request() -> dict:
    """
    Creating the request body for /timer api with invalid url
    :return: request body in dict
    """
    _request = {"hours":1,
        "minutes":1,
        "seconds":1,
        "url":"https://www/google.com"
    }
    return _request