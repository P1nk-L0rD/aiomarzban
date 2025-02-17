import os

import pytest
from dotenv import load_dotenv

from aiomarzban import MarzbanAPI


@pytest.fixture
async def api_client():
    load_dotenv()

    client = MarzbanAPI(
        address=os.getenv("MARZBAN_ADDRESS"),
        username=os.getenv("MARZBAN_USERNAME"),
        password=os.getenv("MARZBAN_PASSWORD"),
    )

    yield client
