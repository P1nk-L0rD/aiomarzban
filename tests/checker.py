import asyncio
import json
import os
import time
import requests

from dotenv import load_dotenv

from aiomarzban import MarzbanAPI, UserStatusCreate, UserDataLimitResetStrategy, UserStatus
from aiomarzban.enums import UserStatusModify
from aiomarzban.utils import future_unix_time

load_dotenv()

url = os.getenv("MARZBAN_ADDRESS")

client = MarzbanAPI(
    address=url,
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
    # with open("cfg.json") as f:
    #     new_cfg = json.load(f)
    # data = await client.modify_core_config(new_cfg)
    # print(data)
    # data = await client.add_node(
    #     name="test4",
    #     address="2.2.5.8",
    #     usage_coefficient=1.1
    # )
    # data = await client.modify_user(
    #     username="test_user",
    #     expire=future_unix_time(minutes=1)
    # )
    # data = await client.get_users(
    #     status=UserStatus.disabled.value
    # )
    # data = await client.modify_user(
    #     username="test_user",
    #     status=UserStatusModify.disabled,
    # )
    # data = await client.remove_admin("second")
    # data = await client.add_user(
    #     username="my_user",
    #     expire=future_unix_time(days=-1),
    #     proxies={"vless": {"flow": ""}},
    # )
    # print(data)
    templates = await client.get_user_templates()
    for template in templates:
        await client.remove_user_template(template.id)
        print(f"User {template.username} deleted successfully.")


if __name__ == "__main__":
    asyncio.run(main())
