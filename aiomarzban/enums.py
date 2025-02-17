from enum import Enum


class Methods(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


class UserStatusCreate(str, Enum):
    active = "active"
    on_hold = "on_hold"


class UserStatusModify(str, Enum):
    active = "active"
    disabled = "disabled"
    on_hold = "on_hold"


class UserStatus(str, Enum):
    active = "active"
    on_hold = "on_hold"
    disabled = "disabled"
    limited = "limited"
    expired = "expired"


class UserDataLimitResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class NodeStatus(str, Enum):
    connected = "connected"
    connecting = "connecting"
    error = "error"
    disabled = "disabled"


class ProxyHostSecurity(str, Enum):
    inbound_default = "inbound_default"
    none = "none"
    tls = "tls"


class ProxyHostALPN(str, Enum):
    none = ""
    h3 = "h3"
    h2 = "h2"
    http1_1 = "http/1.1"
    h3_h2_http1_1 = "h3,h2,http/1.1"
    h3_h2 = "h3,h2"
    h2_http1_1 = "h2,http/1.1"


class ProxyHostFingerprint(str, Enum):
    none = ""
    chrome = "chrome"
    firefox = "firefox"
    safari = "safari"
    ios = "ios"
    android = "android"
    edge = "edge"
    _360 = "360"
    qq = "qq"
    random = "random"
    randomized = "randomized"


class ProxyTypes(str, Enum):
    vmess = "vmess"
    vless = "vless"
    trojan = "trojan"
    shadowsocks = "shadowsocks"


