import asyncio
import datetime
import logging

import uvloop
from arq.worker import Worker

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# -------- background tasks --------
async def request_url(ctx: Worker, url: str) -> str:
    """
    The function requests the URL using requests library
    :param ctx: main class for running jobs
    :type Worker
    :param url: webserver url to fetch the data from
    :type str

    :rtype: str
    :return: string with the statement data extracted
    """
    await asyncio.sleep(5)
    retry_strategy = Retry(
        total=4,  # Maximum number of retries
        status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
        backoff_factor=2,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('https://', adapter)
    resp = session.get(url)
    return f"Extracted data from {url}"


# -------- base functions --------
async def startup(ctx: Worker) -> None:
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")