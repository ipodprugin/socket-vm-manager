import asyncio
import logging

from server.server import Server
from config import settings


logging.basicConfig(level=logging.INFO)
server = Server(
    host=settings.SERVER_HOST, 
    port=settings.SERVER_PORT, 
    db_uri=settings.DB_URL.get_secret_value(),
)
asyncio.run(server.start())

