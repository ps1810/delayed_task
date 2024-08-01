from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from arq import create_pool
from arq.connections import RedisSettings
from src.app.core.utils import queue
from src.app.main import app
from src.app.core.config import settings

@pytest.fixture(scope='session')
def client() -> Generator[TestClient, Any, None]:
    """
    Creting a test client for testing
    :return:
    """
    with TestClient(app) as _client:
        yield _client

@pytest.fixture
def redis() -> Any:
    """
    Setting up the queue for testing
    :return:
    """
    queue.pool = create_pool(RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT))
    yield queue
    queue.pool.close()