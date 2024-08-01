from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing import Annotated
import re
from ..exceptions.custom_exceptions import ModelValidationError


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


class TimerRequest(BaseModel):
    """
    Request model for API's
    """
    hours: int
    minutes: int
    seconds: int
    url: Annotated[str, AfterValidator(url_validator)]


