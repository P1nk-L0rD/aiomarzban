import asyncio
import os

from load_dotenv import load_dotenv

from aiomarzban.api import MarzbanAPI

load_dotenv()

MARZBAN_ADDRESS = os.getenv("MARZBAN_ADDRESS")
MARZBAN_USERNAME = os.getenv("MARZBAN_USERNAME")
MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD")


marzban = MarzbanAPI(
    address=MARZBAN_ADDRESS,
    username=MARZBAN_USERNAME,
    password=MARZBAN_PASSWORD,
)
