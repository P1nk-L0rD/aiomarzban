import copy
import datetime
from typing import Optional, Union, List, Any, Set

import aiohttp
import requests

from .utils import current_unix_utc_time, future_unix_time, unix_time_delta, gb_to_bytes
from .enums import UserStatus, UserDataLimitResetStrategy
from .exceptions import MarzbanException
from .methods import Methods


class MarzbanAPI:
    def __init__(
        self,
        address: str,
        username: str,
        password: str,
        default_days: Optional[int] = 0,
        default_data_limit: Optional[int] = 0,
        default_data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = UserDataLimitResetStrategy.no_reset,
        default_proxies: Optional[dict] = None,
        default_inbounds: Optional[dict] = None,
    ):
        self.address = address
        self.api_address = address + "api"
        self.username = username
        self.password = password
        self.token = self.get_token()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        # Default params
        self.default_days = default_days
        self.default_data_limit = default_data_limit
        self.default_data_limit_reset_strategy = default_data_limit_reset_strategy
        self.default_proxies = default_proxies or dict()
        self.default_inbounds = default_inbounds or dict()

    def get_token(self) -> str:
        """Создание токена доступа."""
        data = {
            "username": self.username,
            "password": self.password
        }
        answer = requests.post(self.api_address + "/admin/token", data=data)
        if answer.status_code != 200:
            raise MarzbanException(f"Error: {answer.status_code}; Body: {answer.json()}")

        data = answer.json()
        return data["access_token"]

    def refresh_token(self):
        """Обновление токена доступа."""
        print("REFRESHING TOKEN...")
        self.token = self.get_token()
        self.headers["Authorization"] = f"Bearer {self.token}"

    async def _make_request(self, method, path: str, data: dict = None):
        """Функция для создания запросов к серверу."""
        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.api_address + path, json=data, headers=self.headers) as resp:
                if 200 <= resp.status < 300:
                    body = await resp.json()
                    return body

                elif resp.status == 401:
                    print(str(resp.text()))
                    self.refresh_token()

                else:
                    raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")

# ADMIN

    async def