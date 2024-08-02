from .api import router
from .core.config import settings
from .core.setup import create_application
import logging

logging.basicConfig(filename="./logging.conf")

app = create_application(router=router, settings=settings)