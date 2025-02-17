import asyncio
import os

from dotenv import load_dotenv

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


async def main():
    admins = await marzban.get_admins()
    print(admins)
    data = await marzban.modify_admin(username="admin", is_sudo=False, telegram_id=1)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())

