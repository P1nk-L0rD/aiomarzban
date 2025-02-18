from typing import Optional, List, Union, Dict, Any

from pydantic import BaseModel

from aiomarzban.enums import NodeStatus, ProxyHostSecurity, ProxyHostFingerprint, ProxyHostALPN, ProxyTypes, \
    UserDataLimitResetStrategy, UserStatus, UserStatusCreate, UserStatusModify


# ADMIN

class Admin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None
    users_usage: Optional[int] = None


class AdminCreate(Admin):
    password: str


class AdminModify(BaseModel):
    password: Optional[str] = None
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None

# CORE

class CoreStats(BaseModel):
    version: str
    started: bool
    logs_websocket: str


class Forbidden(BaseModel):
    ...

class HTTPException(BaseModel):
    ...

class HTTPValidationError(BaseModel):
    ...


class NextPlanModel(BaseModel):
    data_limit: Optional[int] = None
    expire: Optional[int] = None
    add_remaining_traffic: Optional[bool] = False

# NODES


class NodeBase(BaseModel):
    name: str
    address: str
    port: Optional[int] = 62050
    api_port: Optional[int] = 62051
    usage_coefficient: Optional[float] = 1


class NodeCreate(NodeBase):
    add_as_new_host: Optional[bool] = True


class NodeModify(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    api_port: Optional[int] = None
    usage_coefficient: Optional[float] = None
    status: Optional[NodeStatus] = None


class NodeResponse(NodeBase):
    id: int
    xray_version: Optional[str] = None
    status: NodeStatus = None
    message: Optional[str] = None


class NodeSettings(BaseModel):
    min_node_version: Optional[str] = "v0.2.0"
    certificate: str


class NodeUsageResponse(BaseModel):
    node_id: Optional[int] = None
    node_name: str
    uplink: int
    downlink: int


class NodesUsageResponse(BaseModel):
    usages: List[NodeUsageResponse]


class NotFound(BaseModel):
    detail: Optional[str] = None


class ProxyHost(BaseModel):
    remark: str
    address: str
    port: Optional[int] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    security: Optional[ProxyHostSecurity] = ProxyHostSecurity.inbound_default
    alpn: Optional[ProxyHostALPN] = ProxyHostALPN.none
    fingerprint: Optional[ProxyHostFingerprint] = ProxyHostFingerprint.none
    allow_insecure: Optional[bool] = None
    is_disabled: Optional[bool] = None
    mux_enable: Optional[bool] = None
    fragment_setting: Optional[str] = None
    noise_setting: Optional[str] = None
    random_user_agent: Optional[bool] = None
    use_sni_as_host: Optional[bool] = None


class ProxyInbound(BaseModel):
    tag: str
    protocol: ProxyTypes
    network: str
    tls: str
    port: Union[int, str]


class SubscriptionUserResponse(BaseModel):
    proxies: Dict[str, Any]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataLimitResetStrategy = UserDataLimitResetStrategy.no_reset
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    next_plan: Optional[NextPlanModel] = None
    username: str
    status: UserStatus
    used_traffic: int
    lifetime_used_traffic: int = 0
    created_at: str
    links: List[str] = []
    subscription_url: str = ""


class SystemStats(BaseModel):
    version: str
    mem_total: int
    mem_used: int
    cpu_cores: int
    cpu_usage: float
    total_user: int # TODO: should be total_users
    online_users: int
    users_active: int
    users_on_hold: int
    users_disabled: int
    users_expired: int
    users_limited: int
    incoming_bandwidth: int
    outgoing_bandwidth: int
    incoming_bandwidth_speed: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Unauthorized(BaseModel):
    detail: Optional[str] = "Not authenticated"


# USER

class UserCreate(BaseModel):
    proxies: Dict[str, Any]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = UserDataLimitResetStrategy.no_reset
    inbounds: Optional[Dict[str, List[str]]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    auto_delete_in_days: Optional[int] = None
    next_plan: Optional[NextPlanModel] = None
    username: str
    status: Optional[UserStatusCreate] = None


class UserModify(BaseModel):
    proxies: Optional[Dict[str, Any]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Optional[Dict[str, List[str]]] = None
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[str] = None
    auto_delete_in_days: Optional[int] = None
    next_plan: Optional[NextPlanModel] = None
    status: Optional[UserStatusModify] = None


class UserResponse(BaseModel):
    proxies: Dict[str, Any]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataLimitResetStrategy = UserDataLimitResetStrategy.no_reset
    inbounds: Dict[str, List[str]] = {}
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    auto_delete_in_days: Optional[int] = None
    next_plan: Optional[NextPlanModel] = None
    username: str
    status: UserStatus
    used_traffic: int
    lifetime_used_traffic: Optional[int] = 0
    created_at: str
    links: List[str] = []
    subscription_url: str = ""
    excluded_inbounds: Dict[str, Any] = {}
    admin: Optional[Admin] = None


class UserTemplateCreate(BaseModel):
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[str, List[str]]] = {}


class UserTemplateModify(UserTemplateCreate):
    ...


class UserTemplateResponse(UserTemplateCreate):
    id: int


class UserUsageResponse(BaseModel):
    node_id: Optional[int] = None
    node_name: str
    used_traffic: int


class UserUsagesResponse(BaseModel):
    username: str
    usages: List[UserUsageResponse]


class UsersResponse(BaseModel):
    users: List[UserResponse]
    total: int


class UsersUsagesResponse(BaseModel):
    usages: List[UserUsagesResponse]


class ValidationError(BaseModel):
    loc: Any
    msg: str
    type: str


class SetOwner(BaseModel):
    admin_username: str
