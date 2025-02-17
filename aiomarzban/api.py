import copy
import datetime
from typing import Optional, Union, List, Any, Set

import aiohttp
import requests

from .utils import current_unix_utc_time, future_unix_time, unix_time_delta, gb_to_bytes
from .enums import UserStatus, UserDataLimitResetStrategy
from .models import Admin, AdminCreate, AdminModify
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

    async def _make_request(self, method, path: str, data: dict = None, params: dict = None):
        """Функция для создания запросов к серверу."""
        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.api_address + path, json=data, headers=self.headers, params=params) as resp:
                if 200 <= resp.status < 300:
                    body = await resp.json()
                    return body

                elif resp.status == 401:
                    print(str(resp.text()))
                    self.refresh_token()
                    await self._make_request(method, path, data=data)

                else:
                    raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")

# ADMIN

    async def get_current_admin(self) -> Admin:
        resp = await self._make_request(Methods.GET, "/admin")
        return Admin(**resp)

    async def create_admin(
        self,
        username: str,
        password: str,
        is_sudo: bool,
        telegram_id: Optional[int] = None,
        discord_webhook: Optional[str] = None,
        users_usage: Optional[int] = 0,
    ) -> Admin:
        data = AdminCreate(
            username=username,
            password=password,
            is_sudo=is_sudo,
            telegram_id=telegram_id,
            discord_webhook=discord_webhook,
            users_usage=users_usage,
        )
        resp = await self._make_request(Methods.POST, "/admin", data=data.model_dump())
        return Admin(**resp)

    async def modify_admin(
        self,
        username: str,
        is_sudo: bool,
        password: Optional[str] = None,
        telegram_id: Optional[int] = None,
        discord_webhook: Optional[str] = None,
    ) -> Admin:
        data = AdminModify(
            password=password,
            is_sudo=is_sudo,
            telegram_id=telegram_id,
            discord_webhook=discord_webhook,
        )
        resp = await self._make_request(Methods.PUT, f"/admin/{username}", data=data.model_dump())
        return Admin(**resp)

    async def remove_admin(self, username: str) -> None:
        return await self._make_request(Methods.DELETE, f"admin/{username}")

    async def get_admins(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[str] = None,
    ):
        params = {"offset": offset, "limit": limit, "username": username}
        resp = await self._make_request(Methods.GET, "/admins", params=params)
        return [Admin(**data) for data in resp]

    async def disable_all_active_users(self, username: str) -> None:
        return await self._make_request(Methods.POST, f"admin/{username}/users/disable")

    async def activate_all_disabled_users(self, username: str) -> None:
        return await self._make_request(Methods.POST, f"admin/{username}/users/activate")

    async def reset_admin_usage(self, username: str) -> Admin:



