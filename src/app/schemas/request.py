from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing import Annotated
import re
from ..exceptions.custom_exceptions import ModelValidationError
from ..core.utils.logger import get_logger

logger = get_logger(__name__)

def url_validator(url) -> str:
    """
    The function validates if a url is valid
    :param url: url in request
    :type: str

    :rtype: str
    :return: url if is valid otherwise raise error
    """
    url_regex = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
    match_object = url_regex.search(url)
    if match_object is None:
        raise ModelValidationError("Invalid URL")
    return url


def check_negative(value) -> int:
    """
    The function validates if hours, mintues and seconds are greater than 0
    :param value: it can be hours, minutes or seconds
    :type int

    :rtype: int
    :return: return the value if it is greater than or equal to 0
    """
    if value < 0:
        logger.error(f"Value is negative")
        raise ValueError("Value should be greater than 0")
    return value


class TimerRequest(BaseModel):
    """
    Request model for API's
    """
    hours: Annotated[int, AfterValidator(check_negative)]
    minutes: Annotated[int, AfterValidator(check_negative)]
    seconds: Annotated[int, AfterValidator(check_negative)]
    url: Annotated[str, AfterValidator(url_validator)]


