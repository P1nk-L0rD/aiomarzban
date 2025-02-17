from typing import Optional, List, Any, Dict

import aiohttp
import requests

from .enums import UserDataLimitResetStrategy
from .utils import remove_nones
from .exceptions import MarzbanException
from .methods import Methods
from .models import Admin, AdminCreate, AdminModify, CoreStats, NodeCreate, NodeModify, NodeResponse, NodeSettings, \
    NodeStatus, NodesUsageResponse, SubscriptionUserResponse, SystemStats, ProxyInbound, ProxyHost, \
    UserTemplateResponse, UserTemplateCreate, UserTemplateModify, NextPlanModel, UserStatusCreate, UserCreate, \
    UserModify, UserResponse, UserStatusModify, UserStatus, UsersResponse, UserUsageResponse, UsersUsagesResponse


class MarzbanAPI:
    def __init__(
        self,
        address: str,
        username: str,
        password: str,
        sub_path: Optional[str] = "sub",

        # Default user params
        default_days: Optional[int] = None,
        default_expire: Optional[int] = None,
        default_data_limit: Optional[int] = None,
        default_data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None,
        default_proxies: Optional[dict] = None,
        default_inbounds: Optional[Dict[str, Any]] = None,
        default_note: Optional[str] = None,
        default_on_hold_expire_duration: Optional[int] = None,
        default_on_hold_timeout: Optional[str] = None,
        default_auto_delete_in_days: Optional[int] = None,
        default_next_plan: Optional[NextPlanModel] = None,
        default_status: Optional[UserStatusCreate] = None,
    ):
        self.address = address
        self.api_url = address + "api"
        self.username = username
        self.password = password
        self.sub_path = sub_path
        self.token = self.get_token()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        # Default user params
        self.default_days = default_days
        self.default_expire = default_expire
        self.default_data_limit = default_data_limit
        self.default_data_limit_reset_strategy = default_data_limit_reset_strategy
        self.default_proxies = default_proxies or dict()
        self.default_inbounds = default_inbounds or dict()
        self.default_note = default_note
        self.default_on_hold_expire_duration = default_on_hold_expire_duration
        self.default_on_hold_timeout = default_on_hold_timeout
        self.default_auto_delete_in_days = default_auto_delete_in_days
        self.default_next_plan = default_next_plan
        self.default_status = default_status

    def get_token(self) -> str:
        """Bearer token creation."""
        data = {
            "username": self.username,
            "password": self.password,
        }
        answer = requests.post(self.api_url + "/admin/token", data=data)
        if answer.status_code != 200:
            raise MarzbanException(f"Error: {answer.status_code}; Body: {answer.json()}")

        return answer.json()["access_token"]

    def refresh_token(self):
        """Bearer token refreshing."""
        print("REFRESHING TOKEN...")
        self.token = self.get_token()
        self.headers["Authorization"] = f"Bearer {self.token}"

    async def _request(
        self,
        method: str,
        path: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        api_url: str = None,
    ):
        """Async requests to server via HTTP."""

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url=(api_url or self.api_url) + path,
                json=data,
                headers=headers or self.headers,
                params=params,
                ssl=False,
            ) as resp:
                if 200 <= resp.status < 300:
                    body = await resp.json()
                    return body

                elif resp.status == 401:
                    print(str(resp.text()))
                    self.refresh_token()
                    await self._request(method, path, data=data)

                else:
                    raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")

# ADMIN

    async def get_current_admin(self) -> Admin:
        resp = await self._request(Methods.GET, "/admin")
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
        resp = await self._request(Methods.POST, "/admin", data=data.model_dump())
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
        resp = await self._request(Methods.PUT, f"/admin/{username}", data=data.model_dump())
        return Admin(**resp)

    async def remove_admin(self, username: str) -> None:
        return await self._request(Methods.DELETE, f"/admin/{username}")

    async def get_admins(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[str] = None,
    ):
        params = {
            "offset": offset,
            "limit": limit,
            "username": username,
        }
        params = remove_nones(params)
        resp = await self._request(Methods.GET, "/admins", params=params)
        return [Admin(**data) for data in resp]

    async def disable_all_active_users(self, username: str) -> None:
        return await self._request(Methods.POST, f"/admin/{username}/users/disable")

    async def activate_all_disabled_users(self, username: str) -> None:
        return await self._request(Methods.POST, f"/admin/{username}/users/activate")

    async def reset_admin_usage(self, username: str) -> Admin:
        resp = await self._request(Methods.POST, f"/admin/usage/reset/{username}")
        return Admin(**resp)

    async def get_admin_usage(self, username: str) -> int:
        return await self._request(Methods.GET, f"/admin/usage/{username}")

# CORE

    async def get_core_stats(self) -> CoreStats:
        resp = await self._request(Methods.GET, "/core")
        return CoreStats(**resp)

    async def restart_core(self) -> None:
        return await self._request(Methods.POST, "/core/restart")

    async def get_core_config(self) -> dict:
        return await self._request(Methods.GET, "/core/config")

    async def modify_core_config(self, config: dict) -> dict:
        resp = await self._request(Methods.PUT, "/core/config", data=config)
        return resp.json()

# NODE

    async def get_node_settings(self) -> NodeSettings:
        resp = await self._request(Methods.GET, "/node/settings")
        return NodeSettings(**resp)

    async def add_node(
        self,
        name: str,
        address: str,
        port: Optional[int] = 62050,
        api_port: Optional[int] = 62051,
        usage_coefficient: Optional[float] = 1,
        add_as_new_host: Optional[bool] = False,
    ) -> NodeResponse:
        data = NodeCreate(
            name=name,
            address=address,
            port=port,
            api_port=api_port,
            usage_coefficient=usage_coefficient,
            add_as_new_host=add_as_new_host,
        )
        resp = await self._request(Methods.POST, "/node", data=data.model_dump())
        return NodeResponse(**resp)

    async def get_node(self, node_id: int) -> NodeResponse:
        resp = await self._request(Methods.GET, f"/node/{node_id}")
        return NodeResponse(**resp)

    async def modify_node(
        self,
        node_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        port: Optional[int] = None,
        api_port: Optional[int] = None,
        usage_coefficient: Optional[float] = None,
        status: Optional[NodeStatus] = None,
    ) -> NodeResponse:
        data = NodeModify(
            name=name,
            address=address,
            port=port,
            api_port=api_port,
            usage_coefficient=usage_coefficient,
            status=status,
        )
        resp = await self._request(Methods.PUT, f"/node/{node_id}", data=data.model_dump())
        return NodeResponse(**resp)

    async def remove_node(self, node_id: int) -> None:
        return await self._request(Methods.DELETE, f"/node/{node_id}")

    async def get_nodes(self) -> List[NodeResponse]:
        resp = await self._request(Methods.GET, "/nodes")
        return [NodeResponse(**data) for data in resp]

    async def reconnect_node(self, node_id: int) -> None:
        return await self._request(Methods.POST, f"/node/{node_id}/reconnect")

    async def get_node_usage(
        self,
        start: Optional[str] = "",
        end: Optional[str] = "",
    ) -> NodesUsageResponse:
        params = {
            "start": start,
            "end": end,
        }
        params = remove_nones(params)
        resp = await self._request(Methods.GET, "nodes/usage", params=params)
        return NodesUsageResponse(**resp)

# SUBSCRIPTION

    async def user_subscription(self, token: str, user_agent: Optional[str] = "") -> Any:
        headers = {"user-agent": user_agent}
        return await self._request(Methods.GET, f"/{self.sub_path}/{token}", headers=headers)

    async def user_subscription_info(self, token: str) -> SubscriptionUserResponse:
        resp = await self._request(Methods.GET, f"/{self.sub_path}/{token}/info")
        return SubscriptionUserResponse(**resp)

    async def user_get_usage(self, token: str, start: Optional[str] = "", end: Optional[str] = "") -> Any:
        params = {
            "start": start,
            "end": end,
        }
        params = remove_nones(params)
        return await self._request(Methods.GET, f"/{self.sub_path}/{token}/usage", params=params)

    async def user_subscription_with_client_type(
        self,
        client_type: str,
        token: str,
        user_agent: Optional[str] = "",
    ) -> Any:
        headers = {"user-agent": user_agent}
        return await self._request(Methods.GET, f"{self.sub_path}/{token}/{client_type}", headers=headers)

# SYSTEM

    async def get_system_stats(self) -> SystemStats:
        resp = await self._request(Methods.GET, "/system")
        return SystemStats(**resp)

    async def get_inbounds(self) -> Dict[str, List[ProxyInbound]]:
        return await self._request(Methods.GET, "/inbounds")

    async def get_hosts(self) -> Dict[str, List[ProxyHost]]:
        return await self._request(Methods.GET, "/hosts")

    async def modify_hosts(self, hosts: Dict[str, List[ProxyHost]]) -> Dict[str, List[ProxyHost]]:
        return await self._request(Methods.PUT, "/hosts", data=hosts)

# USER TEMPLATES

    async def add_user_template(
        self,
        name: Optional[str] = None,
        data_limit: Optional[int] = None,
        expire_duration: Optional[int] = None,
        username_prefix: Optional[str] = None,
        username_suffix: Optional[str] = None,
        inbounds: Optional[Dict[str, Any]] = None,
    ) -> UserTemplateResponse:
        data = UserTemplateCreate(
            name=name,
            data_limit=data_limit,
            expire_duration=expire_duration,
            username_prefix=username_prefix,
            username_suffix=username_suffix,
            inbounds=inbounds or {},
        )
        resp = await self._request(Methods.POST, "/user_template", data=data.model_dump())
        return UserTemplateResponse(**resp)

    async def get_user_templates(self) -> List[UserTemplateResponse]:
        resp = await self._request(Methods.GET, "/user_template")
        return [UserTemplateResponse(**data) for data in resp]

    async def get_user_template(self, template_id: int) -> UserTemplateResponse:
        resp = await self._request(Methods.GET, f"/user_template/{template_id}")
        return UserTemplateResponse(**resp)

    async def modify_user_template(
        self,
        template_id: int,
        name: Optional[int] = None,
        data_limit: Optional[int] = None,
        expire_duration: Optional[int] = None,
        username_prefix: Optional[str] = None,
        username_suffix: Optional[str] = None,
        inbounds: Optional[Dict[str, Any]] = None,
    ) -> UserTemplateResponse:
        data = UserTemplateModify(
            name=name,
            data_limit=data_limit,
            expire_duration=expire_duration,
            username_prefix=username_prefix,
            username_suffix=username_suffix,
            inbounds=inbounds,
        )
        resp = await self._request(Methods.PUT, f"/user_template/{template_id}", data=data.model_dump())
        return UserTemplateResponse(**resp)

    async def remove_user_template(self, template_id) -> None:
        return await self._request(Methods.DELETE, f"/user_template/{template_id}")

# USER

    async def add_user(
        self,
        username: str,
        proxies: Optional[Dict[str, List[ProxyHost]]] = None,
        expire: Optional[int] = None,
        data_limit: Optional[int] = None,
        data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None,
        inbounds: Optional[Dict[str, Any]] = None,
        note: Optional[str] = None,
        sub_updated_at: Optional[str] = None,
        sub_last_user_agent: Optional[str] = None,
        online_at: Optional[str] = None,
        on_hold_expire_duration: Optional[int] = None,
        on_hold_timeout: Optional[str] = None,
        auto_delete_in_days: Optional[int] = None,
        next_plan: Optional[NextPlanModel] = None,
        status: Optional[UserStatusCreate] = None,
    ) -> UserResponse:
        data = UserCreate(
            proxies=proxies,
            expire=expire,
            data_limit=data_limit,
            data_limit_reset_strategy=data_limit_reset_strategy,
            inbounds=inbounds,
            note=note,
            sub_updated_at=sub_updated_at,
            sub_last_user_agent=sub_last_user_agent,
            online_at=online_at,
            on_hold_expire_duration=on_hold_expire_duration,
            on_hold_timeout=on_hold_timeout,
            auto_delete_in_days=auto_delete_in_days,
            next_plan=next_plan,
            username=username,
            status=status,
        )

        resp = await self._request(Methods.POST, "/user", data=data.model_dump())
        return UserResponse(**resp)

    async def get_user(self, username: Any) -> UserResponse:
        resp = await self._request(Methods.GET, f"/user/{username}")
        return UserResponse(**resp)

    async def modify_user(
        self,
        username: str,
        proxies: Optional[Dict[str, List[ProxyHost]]] = None,
        expire: Optional[int] = None,
        data_limit: Optional[int] = None,
        data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None,
        inbounds: Optional[Dict[str, Any]] = None,
        note: Optional[str] = None,
        sub_updated_at: Optional[str] = None,
        sub_last_user_agent: Optional[str] = None,
        online_at: Optional[str] = None,
        on_hold_expire_duration: Optional[int] = None,
        on_hold_timeout: Optional[str] = None,
        auto_delete_in_days: Optional[int] = None,
        next_plan: Optional[NextPlanModel] = None,
        status: Optional[UserStatusModify] = None,
    ) -> UserResponse:
        data = UserModify(
            proxies=proxies,
            expire=expire,
            data_limit=data_limit,
            data_limit_reset_strategy=data_limit_reset_strategy,
            inbounds=inbounds,
            note=note,
            sub_updated_at=sub_updated_at,
            sub_last_user_agent=sub_last_user_agent,
            online_at=online_at,
            on_hold_expire_duration=on_hold_expire_duration,
            on_hold_timeout=on_hold_timeout,
            auto_delete_in_days=auto_delete_in_days,
            next_plan=next_plan,
            status=status,
        )
        resp = await self._request(Methods.PUT, f"/user/{username}", data=data.model_dump())
        return UserResponse(**resp)

    async def remove_user(self, username: Any) -> None:
        return await self._request(Methods.DELETE, f"/user/{username}")

    async def reset_user_usage_data(self, username: Any) -> UserResponse:
        resp = await self._request(Methods.POST, f"/user/{username}/reset")
        return UserResponse(**resp)

    async def revoke_user_subscription(self, username: Any) -> UserResponse:
        resp = await self._request(Methods.POST, f"/user/{username}/revoke_sub")
        return UserResponse(**resp)

    async def get_users(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[List[str]] = None,
        search: Optional[str] = None,
        admin: Optional[List[str]] = None,
        status: Optional[UserStatus] = None,
        sort: Optional[str] = None,
    ) -> UsersResponse: # TODO: check method
        params = {
            "offset": offset,
            "limit": limit,
            "username": username,
            "search": search,
            "admin": admin,
            "status": status,
            "sort": sort,
        }
        remove_nones(params)
        resp = await self._request(Methods.GET, "/users", params=params)
        return UsersResponse(**resp)

    async def reset_users_usage_data(self) -> None:
        return await self._request(Methods.POST, "/users/reset")

    async def get_user_usage(
        self,
        username: Any,
        start: Optional[str] = "",
        end: Optional[str] = "",
    ) -> UserUsageResponse:
        params = {
            "start": start,
            "end": end,
        }
        params = remove_nones(params)
        resp = await self._request(Methods.GET, f"/user/{username}/usage", params=params)
        return UserUsageResponse(**resp)

    async def active_next_plan(self, username: Any) -> UserResponse:
        resp = await self._request(Methods.POST, f"/user/{username}/active-next")
        return UserResponse(**resp)

    async def get_users_usage(
        self,
        start: Optional[str] = "",
        end: Optional[str] = "",
        admin: Optional[List[str]] = None,
    ) -> UsersUsagesResponse:
        params = {
            "start": start,
            "end": end,
            "admin": admin,
        }
        params = remove_nones(params)
        resp = await self._request(Methods.GET, "/users/usage", params=params)
        return UsersUsagesResponse(**resp)

    async def set_owner(self, username: str, admin_username: Any) -> UserResponse:
        data = {"admin_username": str(admin_username)}
        resp = await self._request(Methods.PUT, f"/user/{username}/set-owner", data=data)
        return UserResponse(**resp)

    async def get_expired_users(
        self,
        expired_after: Optional[str] = None,
        expired_before: Optional[str] = None,
    ) -> UsersResponse: # TODO: check returned data
        params = {
            "expired_after": expired_after,
            "expired_before": expired_before,
        }
        params = remove_nones(params)
        resp = await self._request(Methods.GET, "/users/expired", params=params)
        return UsersResponse(**resp)

    async def delete_expired_users(
        self,
        expired_after: Optional[str] = None,
        expired_before: Optional[str] = None,
    ) -> None:
        params = {
            "expired_after": expired_after,
            "expired_before": expired_before,
        }
        params = remove_nones(params)
        return await self._request(Methods.DELETE, "/users/expired", params=params)
