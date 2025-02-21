import copy
import datetime
from asyncio.exceptions import TimeoutError
from http import HTTPStatus
from typing import Optional, List, Any, Dict

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

from .enums import UserDataLimitResetStrategy, Methods
from .exceptions import MarzbanException
from .models import Admin, AdminCreate, AdminModify, CoreStats, NodeCreate, NodeModify, NodeResponse, NodeSettings, \
    NodeStatus, NodesUsageResponse, SubscriptionUserResponse, SystemStats, ProxyInbound, ProxyHost, \
    UserTemplateResponse, UserTemplateCreate, UserTemplateModify, NextPlanModel, UserStatusCreate, UserCreate, \
    UserModify, UserResponse, UserStatusModify, UserStatus, UsersResponse, UserUsageResponse, UsersUsagesResponse, \
    SetOwner, OffsetLimitUsernameParams, StartEndParams, GetUsersParams, ExpiredBeforeAfterParams, StartEndAdminParams, \
    AdminTokenPost, AdminTokenAnswer
from .utils import future_unix_time, gb_to_bytes, current_unix_utc_time, unix_time_delta


class MarzbanAPI:
    def __init__(
        self,
        address: str,
        username: str,
        password: str,
        sub_path: Optional[str] = "sub",

        # Default user params
        default_days: Optional[int] = None,
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

        # Token settings
        grant_type: Optional[str] = None,
        scope: Optional[str] = "",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,

        # Request settings
        timeout: Optional[int] = 10,
        retries: Optional[int] = 1,
    ):
        """
        Provide password, username and password to create api client.

        :param address: Panel address. Example: https://marzban.com/ (without /api).
        :param username: Marzban username.
        :param password: Marzban password.
        :param sub_path: Path to the subscription url.
        :param default_days: Default number of subscription days when creating a user.
        :param default_data_limit: Default data limit in GB (GigaBytes) when creating a user.
        :param default_data_limit_reset_strategy: Default data limit strategy when creating a user.
        :param default_proxies: Default proxies when creating a user.
        :param default_inbounds: Default inbounds when creating a user.
        :param default_note: Default note when creating a user.
        :param default_on_hold_expire_duration: Default on hold expire duration.
        :param default_on_hold_timeout: Default on hold timeout.
        :param default_auto_delete_in_days: Default auto delete in days.
        :param default_next_plan: Default next plan.
        :param default_status: Default user status.
        :param grant_type: Grant type.
        :param scope: Scope.
        :param client_id: Client ID.
        :param client_secret: Client Secret.
        :param timeout: Default timeout in seconds.
        :param retries: Default number of retries (after first unsuccessful request).
        """
        self.address = address
        self.api_url = address + "api"
        self.username = str(username)
        self.password = str(password)
        self.sub_path = sub_path
        self.headers = None
        self.encoded_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Default user params
        self.default_days = default_days
        self.default_data_limit = gb_to_bytes(default_data_limit)
        self.default_data_limit_reset_strategy = default_data_limit_reset_strategy or UserDataLimitResetStrategy.no_reset
        self.default_proxies = default_proxies or dict()
        self.default_inbounds = default_inbounds or dict()
        self.default_note = default_note
        self.default_on_hold_expire_duration = default_on_hold_expire_duration
        self.default_on_hold_timeout = default_on_hold_timeout
        self.default_auto_delete_in_days = default_auto_delete_in_days
        self.default_next_plan = default_next_plan
        self.default_status = default_status or UserStatus.active

        # Token settings
        self.token_data = AdminTokenPost(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )

        # Request settings
        self.timeout = timeout
        self.retries = retries

    async def _async_request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        not_json_data: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_url: Optional[str] = None,
        timeout: Optional[int] = None,
        allow_empty_headers: Optional[bool] = False,
    ):
        """Async requests to server via HTTP."""

        if headers is None and self.headers is None and not allow_empty_headers:
            await self.refresh_credentials()

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url=(api_url or self.api_url) + path,
                json=data,
                data=not_json_data,
                headers=headers or self.headers,
                params=params,
                ssl=False,
                timeout=timeout or self.timeout,
            ) as resp:
                ans = await resp.json()
                if HTTPStatus.OK <= resp.status <= HTTPStatus.IM_USED:
                    return ans

                elif resp.status == HTTPStatus.UNAUTHORIZED:
                    error = ans.get("detail")
                    if error == "Could not validate credentials":
                        await self.refresh_credentials()
                        return await self._async_request(method, path, data=data)
                    elif error == "Incorrect username or password":
                        raise MarzbanException(error)
                    raise MarzbanException(f"Auth error: {error}")

                else:
                    raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")

    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        not_json_data: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        api_url: Optional[str] = None,
        timeout: Optional[int] = None,
        allow_empty_headers: Optional[bool] = False,
    ):
        """Send request with retries."""

        for attempt in range(self.retries + 1):
            try:
                return await self._async_request(
                    method=method,
                    path=path,
                    data=data,
                    not_json_data=not_json_data,
                    params=params,
                    headers=headers,
                    api_url=api_url,
                    timeout=timeout,
                    allow_empty_headers=allow_empty_headers,
                )
            except (ClientConnectorError, TimeoutError):
                if attempt < self.retries:
                    continue
                else:
                    raise

# ADMIN

    async def refresh_credentials(self) -> None:
        resp = await self._request(
            Methods.POST, "/admin/token",
            not_json_data=self.token_data.model_dump(exclude_none=True),
            allow_empty_headers=True,
        )
        resp = AdminTokenAnswer(**resp)
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {resp.access_token}"
        }

    async def get_current_admin(self) -> Admin:
        resp = await self._request(Methods.GET, "/admin")
        return Admin(**resp)

    async def create_admin(
        self,
        username: Any,
        password: str,
        is_sudo: Optional[bool] = False,
        telegram_id: Optional[int] = None,
        discord_webhook: Optional[str] = None,
        users_usage: Optional[int] = None,
    ) -> Admin:
        data = AdminCreate(
            username=str(username),
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
        username: Any,
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

    async def remove_admin(self, username: Any) -> None:
        return await self._request(Methods.DELETE, f"/admin/{username}")

    async def get_admins(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[str] = None,
    ):
        params = OffsetLimitUsernameParams(offset=offset, limit=limit, username=username)
        resp = await self._request(Methods.GET, "/admins", params=params.model_dump(exclude_none=True))
        return [Admin(**data) for data in resp]

    async def disable_all_active_users(self, username: Any) -> None:
        return await self._request(Methods.POST, f"/admin/{username}/users/disable")

    async def activate_all_disabled_users(self, username: Any) -> None:
        return await self._request(Methods.POST, f"/admin/{username}/users/activate")

    async def reset_admin_usage(self, username: Any) -> Admin:
        resp = await self._request(Methods.POST, f"/admin/usage/reset/{username}")
        return Admin(**resp)

    async def get_admin_usage(self, username: Any) -> int:
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
        return resp

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

    async def get_nodes_usage(
        self,
        start: Optional[str] = "",
        end: Optional[str] = "",
    ) -> NodesUsageResponse:
        params = StartEndParams(start=start, end=end)
        resp = await self._request(Methods.GET, "nodes/usage", params=params.model_dump(exclude_none=True))
        return NodesUsageResponse(**resp)

# SUBSCRIPTION

    async def user_subscription(self, token: str, user_agent: Optional[str] = "") -> Any:
        headers = {"user-agent": user_agent}
        return await self._request(Methods.GET, f"/{self.sub_path}/{token}", headers=headers)

    async def user_subscription_info(self, token: str) -> SubscriptionUserResponse:
        resp = await self._request(Methods.GET, f"/{self.sub_path}/{token}/info")
        return SubscriptionUserResponse(**resp)

    async def user_get_usage(self, token: str, start: Optional[str] = "", end: Optional[str] = "") -> Any:
        params = StartEndParams(start=start, end=end)
        return await self._request(Methods.GET, f"/{self.sub_path}/{token}/usage", params=params.model_dump(exclude_none=True))

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

# USER TEMPLATE

    async def add_user_template(
        self,
        name: Optional[Any] = None,
        data_limit: Optional[int] = None,
        expire_duration: Optional[int] = None,
        username_prefix: Optional[str] = None,
        username_suffix: Optional[str] = None,
        inbounds: Optional[Dict[str, Any]] = None,
    ) -> UserTemplateResponse:
        data = UserTemplateCreate(
            name=str(name),
            data_limit=gb_to_bytes(data_limit),
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
            data_limit=gb_to_bytes(data_limit),
            expire_duration=expire_duration,
            username_prefix=username_prefix,
            username_suffix=username_suffix,
            inbounds=inbounds or dict(),
        )
        resp = await self._request(Methods.PUT, f"/user_template/{template_id}", data=data.model_dump(exclude_none=True))
        return UserTemplateResponse(**resp)

    async def remove_user_template(self, template_id) -> None:
        return await self._request(Methods.DELETE, f"/user_template/{template_id}")

# USER

    async def add_user(
        self,
        username: Any,
        proxies: Optional[Dict[str, Any]] = None,
        expire: Optional[int] = None,
        days: Optional[int] = None,
        data_limit: Optional[int] = None,
        data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = UserDataLimitResetStrategy.no_reset,
        inbounds: Optional[Dict[str, Any]] = None,
        note: Optional[str] = None,
        sub_updated_at: Optional[str] = None,
        sub_last_user_agent: Optional[str] = None,
        online_at: Optional[str] = None,
        on_hold_expire_duration: Optional[int] = None,
        on_hold_timeout: Optional[str] = None,
        auto_delete_in_days: Optional[int] = None,
        next_plan: Optional[NextPlanModel] = None,
        status: Optional[UserStatusCreate] = UserStatusCreate.active,
    ) -> UserResponse:
        """
        Creates a new user with specified or default settings.

        :param username: User username.
        :param proxies: available proxies.
        :param expire: Date of expiration in UNIX UTC time.
        :param days: Alternative for expire. Just specify how many days the subscription will be valid and the
        expiration date will be calculated automatically.
        :param data_limit: Data limit in GB (gigabytes).
        :param data_limit_reset_strategy:
        :param inbounds:
        :param note:
        :param sub_updated_at:
        :param sub_last_user_agent:
        :param online_at:
        :param on_hold_expire_duration:
        :param on_hold_timeout:
        :param auto_delete_in_days:
        :param next_plan:
        :param status:
        :return: `UserResponse`
        """

        if days:
            expire = future_unix_time(days=days)
        elif expire:
            ...
        elif self.default_days:
            expire = future_unix_time(days=self.default_days)

        data = UserCreate(
            proxies=proxies or self.default_proxies,
            expire=expire,
            data_limit=gb_to_bytes(data_limit) or self.default_data_limit,
            data_limit_reset_strategy=(data_limit_reset_strategy or self.default_data_limit_reset_strategy),
            inbounds=inbounds or self.default_inbounds,
            note=note or self.default_note,
            sub_updated_at=sub_updated_at,
            sub_last_user_agent=sub_last_user_agent,
            online_at=online_at,
            on_hold_expire_duration=on_hold_expire_duration or self.default_on_hold_expire_duration,
            on_hold_timeout=on_hold_timeout or self.default_on_hold_timeout,
            auto_delete_in_days=auto_delete_in_days or self.default_auto_delete_in_days,
            next_plan=next_plan or self.default_next_plan,
            username=str(username),
            status=status or self.default_status,
        )

        resp = await self._request(Methods.POST, "/user", data=data.model_dump())
        return UserResponse(**resp)

    async def get_user(self, username: Any) -> UserResponse:
        resp = await self._request(Methods.GET, f"/user/{username}")
        return UserResponse(**resp)

    async def modify_user(
        self,
        username: Any,
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
            data_limit=gb_to_bytes(data_limit),
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
        resp = await self._request(Methods.PUT, f"/user/{username}", data=data.model_dump(exclude_none=True))
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
        timeout: Optional[int] = 40,
    ) -> UsersResponse:
        params = GetUsersParams(
            offset=offset,
            limit=limit,
            username=username,
            search=search,
            admin=admin,
            status=status,
            sort=sort,
        )
        data = params.model_dump(exclude_none=True)
        resp = await self._request(Methods.GET, "/users", params=params.model_dump(exclude_none=True), timeout=timeout)
        return UsersResponse(**resp)

    async def reset_users_usage_data(self) -> None:
        return await self._request(Methods.POST, "/users/reset")

    async def get_user_usage(
        self,
        username: Any,
        start: Optional[str] = "",
        end: Optional[str] = "",
    ) -> UserUsageResponse:
        params = StartEndParams(start=start, end=end)
        resp = await self._request(Methods.GET, f"/user/{username}/usage", params=params.model_dump(exclude_none=True))
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
        params = StartEndAdminParams(
            start=start,
            end=end,
            admin=admin,
        )
        resp = await self._request(Methods.GET, "/users/usage", params=params.model_dump(exclude_none=True))
        return UsersUsagesResponse(**resp)

    async def set_owner(self, username: Any, admin_username: Any) -> UserResponse:
        data = SetOwner(admin_username=admin_username)
        resp = await self._request(Methods.PUT, f"/user/{username}/set-owner", params=data.model_dump())
        return UserResponse(**resp)

    async def get_expired_users(
        self,
        expired_after: Optional[str] = None,
        expired_before: Optional[str] = None,
    ) -> List[str]:
        params = ExpiredBeforeAfterParams(
            expired_after=expired_after,
            expired_before=expired_before,
        )
        return await self._request(Methods.GET, "/users/expired", params=params.model_dump(exclude_none=True))

    async def delete_expired_users(
        self,
        expired_after: Optional[str] = None,
        expired_before: Optional[str] = None,
    ) -> List[str]:
        params = ExpiredBeforeAfterParams(
            expired_after=expired_after,
            expired_before=expired_before,
        )
        return await self._request(Methods.DELETE, "/users/expired", params=params.model_dump(exclude_none=True))

# EXTRA (not default methods)

    async def user_get_or_create(self, username: Any, **kwargs: Any) -> UserResponse:
        try:
            return await self.get_user(username)
        except Exception:
            return await self.add_user(username, **kwargs)

    async def user_add_days(self, username: Any, days: int) -> UserResponse:
        """
        Adds days to users subscription. If the user's subscription has expired,
        it will be issued for the specified number of days from the current moment.

        :param username: User username
        :param days: Amount of days to add to subscription.
        :return: `UserResponse`
        """
        old_user = await self.get_user(username)
        if old_user.expire == 0 or old_user.expire is None:
            return old_user
        elif old_user.expire < current_unix_utc_time():
            new_time = future_unix_time(days=days)
        else:
            new_time = old_user.expire + unix_time_delta(days=days)
        return await self.modify_user(str(username), expire=new_time)

    async def user_set_all_inbounds(self, user: UserResponse) -> UserResponse:
        """
        Allows absolutely all inbounds to the user.

        :param user: The user who needs to be given inbounds.
        :return: `UserResponse`
        """
        old_inbounds = user.inbounds
        inbounds = copy.deepcopy(old_inbounds)
        excluded_inbounds = user.excluded_inbounds

        for inbound in excluded_inbounds:
            if inbound in inbounds:
                inbounds[inbound].extend(excluded_inbounds[inbound])
            else:
                inbounds[inbound] = excluded_inbounds[inbound]

        if old_inbounds == inbounds:
            return user

        return await self.modify_user(user.username, inbounds=inbounds)

    async def get_online_users(self) -> UsersResponse:
        """
        Returns all users currently online.

        :return: `UsersResponse`
        """
        all_users = await self.get_users(status=UserStatus.active)
        online_users = []

        for user in all_users.users:
            if user.online_at is None:
                continue
            user_online = datetime.datetime.fromisoformat(user.online_at)
            time_dif = int(current_unix_utc_time() - user_online.timestamp())
            if time_dif < 60:
                online_users.append(user)
        all_users.users = online_users
        return all_users
