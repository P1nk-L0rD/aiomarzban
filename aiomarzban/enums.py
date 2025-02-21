from enum import Enum


class Methods(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


class UserStatusCreate(str, Enum):
    active = "active"
    on_hold = "on_hold"

    def __str__(self):
        return self.value


class UserStatusModify(str, Enum):
    active = "active"
    disabled = "disabled"
    on_hold = "on_hold"

    def __str__(self):
        return self.value


class UserStatus(str, Enum):
    active = "active"
    on_hold = "on_hold"
    disabled = "disabled"
    limited = "limited"
    expired = "expired"

    def __str__(self):
        return self.value


class UserDataLimitResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"

    def __str__(self):
        return self.value


class NodeStatus(str, Enum):
    connected = "connected"
    connecting = "connecting"
    error = "error"
    disabled = "disabled"

    def __str__(self):
        return self.value


class ProxyHostSecurity(str, Enum):
    inbound_default = "inbound_default"
    none = "none"
    tls = "tls"

    def __str__(self):
        return self.value


class ProxyHostALPN(str, Enum):
    none = ""
    h3 = "h3"
    h2 = "h2"
    http1_1 = "http/1.1"
    h3_h2_http1_1 = "h3,h2,http/1.1"
    h3_h2 = "h3,h2"
    h2_http1_1 = "h2,http/1.1"

    def __str__(self):
        return self.value


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

    def __str__(self):
        return self.value


class ProxyTypes(str, Enum):
    vmess = "vmess"
    vless = "vless"
    trojan = "trojan"
    shadowsocks = "shadowsocks"

    def __str__(self):
        return self.value
