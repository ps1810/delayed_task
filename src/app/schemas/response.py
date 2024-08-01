from datetime import timedelta
from typing import Union

from pydantic import BaseModel

class TimerResponse(BaseModel):
    """
    Response model for the API's
    """
    id: str = None
    time_left: Union[int, timedelta] = None
    error: str = None