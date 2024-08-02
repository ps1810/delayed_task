from arq.connections import RedisSettings

from ...core.config import settings
from .functions import request_url, shutdown, startup

REDIS_QUEUE_HOST = settings.REDIS_QUEUE_HOST
REDIS_QUEUE_PORT = settings.REDIS_QUEUE_PORT


class WorkerSettings:
    """
    Settings that will apply while connecting redis using arq
    """
    functions = [request_url]
    redis_settings = RedisSettings(host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT)
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False
    keep_result = 10
    queue_name = "delayed_task"