import asyncio
import os

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
)


async def main():
    async def test():
        try:
            print("Начало try")
            return "Возвращаем значение"
        finally:
            print("Выполняем finally")

    result = await test()
    print(result)

    ...


if __name__ == "__main__":
    asyncio.run(main())
