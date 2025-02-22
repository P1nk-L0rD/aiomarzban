import asyncio
import os
import time

import pytest
from dotenv import load_dotenv

from aiomarzban import MarzbanAPI
from tests.final import delete_all_data, close_session


@pytest.fixture(autouse=True, scope="function")
def wait_after_test():
    """
    Timeout between requests to server.
    """
    yield
    time.sleep(1)


@pytest.fixture(scope="session")
def get_api_client():
    load_dotenv()

    client = MarzbanAPI(
        address=os.getenv("MARZBAN_ADDRESS"),
        username=os.getenv("MARZBAN_USERNAME"),
        password=os.getenv("MARZBAN_PASSWORD"),
        use_single_session=True,
    )

    yield client
    if not os.getenv("PROD") == "FALSE":
        asyncio.run(delete_all_data(client))
    asyncio.run(close_session(client))
