import asyncio
import json
import os
import requests
import time
import requests

from dotenv import load_dotenv

from aiomarzban import MarzbanAPI, UserStatusCreate, UserDataLimitResetStrategy, UserStatus
from aiomarzban.enums import UserStatusModify
from aiomarzban.utils import future_unix_time

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

import requests


data = {
    "username": username,
    "password": password,
}


ans = requests.post(url + "/api/admin/token", data=data)
token = ans.json().get("access_token")



headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
}

# payload = {
#     "username": "some_user",
#     "status": UserStatusModify.disabled,
# }
#
# disabled_user = requests.put(url + "/api/user/some_user", json=payload, headers=headers)
# print(disabled_user.json().get("status"))
#
# # Reset all users
# # requests.post(url + "/api/users/reset", headers=headers)
# requests.post(url + "/api/admin/usage/reset/marzban", headers=headers)




user = requests.get(url + "/api/user/some_user", headers=headers)
print(user.json().get("admin"))

# payload = {"admin_username": "some_admin"}

updated_user = requests.put(url + "/api/user/some_user/set-owner?admin_username=some_admin", headers=headers)
print(updated_user.json())


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
    # templates = await client.get_user_templates()
    # for template in templates:
    #     await client.remove_user_template(template.id)
    #     print(f"User {template.username} deleted successfully.")

    # users = await client.get_users(status=UserStatus.active.value)
    # user = await client.add_user(
    #     username="some_user",
    # )
    # user = await client.create_admin(
    #     username="some_admin",
    #     password="123",
    # )
    # print(user)

    ...



if __name__ == "__main__":
    asyncio.run(main())
