import asyncio
import os
import time

from dotenv import load_dotenv

from aiomarzban import MarzbanAPI, UserStatusCreate, UserDataLimitResetStrategy

load_dotenv()

client = MarzbanAPI(
    address=os.getenv("MARZBAN_ADDRESS"),
    username=os.getenv("MARZBAN_USERNAME"),
    password=os.getenv("MARZBAN_PASSWORD"),
    default_days=10,
    default_proxies = {
        "vless": {
            "flow": ""
        }
    },
    default_data_limit=10,
)

async def main():
    # data = await client.add_user("4eburek", days=5, data_limit=3)
    data = await client.get_online_users()
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
