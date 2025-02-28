import asyncio
import os
import time

from dotenv import load_dotenv

from aiomarzban import MarzbanAPI

load_dotenv()

url = os.getenv("MARZBAN_ADDRESS")
username = os.getenv("MARZBAN_USERNAME")
password = os.getenv("MARZBAN_PASSWORD")

client = MarzbanAPI(
    address=url,
    username=username,
    password=password,
    default_days=10,
    default_proxies = {
        "vless": {
            "flow": ""
        }
    },
    default_data_limit=10,
    # use_single_session=True,
)


async def not_main():
    users = await client.get_users()
    print(users.total)
    await asyncio.sleep(1)


async def main():
    user = await client.get_or_create_user('2222')

    await client.close()

    # await client.close()
    ...


if __name__ == "__main__":
    asyncio.run(main())
