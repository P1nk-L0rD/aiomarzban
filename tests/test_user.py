import time

from aiomarzban.enums import UserStatus, UserDataLimitResetStrategy
from aiomarzban.utils import future_unix_time, gb_to_bytes
from tests.conftest import get_api_client

user_username = "Test_user"
user_expire = future_unix_time(days=1)
user_data_limit = 5
user_note = "Test note"
user_proxies = {"vless": {"flow": ""}}


async def test_add_user(get_api_client):
    api_client = get_api_client

    user = await api_client.add_user(
        username=user_username,
        expire=user_expire,
        data_limit=user_data_limit,
        note=user_note,
        proxies=user_proxies,
    )

    assert user.username == user_username
    assert user.expire == user_expire
    assert user.data_limit == gb_to_bytes(user_data_limit)
    assert user.note == user_note
    assert user.status == UserStatus.active
    assert user.data_limit_reset_strategy == UserDataLimitResetStrategy.no_reset


async def test_get_user(get_api_client):
    api_client = get_api_client
    user = await api_client.get_user(username=user_username)
    assert user.username == user_username
    assert user.expire == user_expire
    assert user.data_limit == gb_to_bytes(user_data_limit)


new_user_expire = future_unix_time(days=3)
new_user_data_limit = 10
new_user_note = "New test note"


async def test_modify_user(get_api_client):
    api_client = get_api_client
    user = await api_client.modify_user(
        username=user_username,
        expire=new_user_expire,
        data_limit=new_user_data_limit,
        note=new_user_note,
    )
    assert user.username == user_username
    assert user.expire == new_user_expire
    assert user.data_limit == gb_to_bytes(new_user_data_limit)
    assert user.note == new_user_note


async def test_reset_user_data_usage(get_api_client): # TODO: changes user status to active by itself
    api_client = get_api_client
    user = await api_client.reset_user_usage_data(username=user_username)
    assert user.used_traffic == 0


async def test_modify_user_disable(get_api_client):
    api_client = get_api_client
    user = await api_client.modify_user(
        username=user_username,
        status=UserStatus.disabled,
    )
    assert user.status == UserStatus.disabled


async def test_revoke_user_subscription(get_api_client):
    api_client = get_api_client
    await api_client.revoke_user_subscription(username=user_username)


async def test_get_users(get_api_client):
    api_client = get_api_client
    users = await api_client.get_users()
    assert user_username in [user.username for user in users.users]


async def test_get_users_with_params(get_api_client):
    api_client = get_api_client
    users = await api_client.get_users(
        status=UserStatus.disabled.value,
    )
    assert user_username in [user.username for user in users.users]


async def test_reset_users_data_usage(get_api_client):
    api_client = get_api_client
    await api_client.reset_users_usage_data()


# async def test_get_user_usage(get_api_client):
#     api_client = get_api_client
#     usage = await api_client.get_user_usage(username=user_username)
#
#
# async def test_active_next_plan(get_api_client):
#     api_client = get_api_client
#     user = await api_client.active_next_plan()
#
#
# async def test_get_users_usage(get_api_client):
#     api_client = get_api_client
#     usages = await api_client.get_users_usage()


# async def test_set_owner(get_api_client): # TODO: not working in marzban
#     api_client = get_api_client
#
#     user = await api_client.get_user(username=user_username)
#     current_admin = await api_client.get_current_admin()
#     assert user.admin.username == current_admin.username
#
#     time.sleep(0.5)
#     new_admin = await api_client.create_admin(username="second", password="<PASSWORD>")
#     user = await api_client.set_owner(username=user_username, admin_username=new_admin.username)
#     assert user.admin.username == new_admin.username
#
#     time.sleep(0.5)
#     await api_client.set_owner(username=user_username, admin_username=current_admin.username)
#     await api_client.remove_admin(new_admin.username)


expired_user_username = "Expired_user"
expired_user_expire = future_unix_time(days=-1)


async def test_add_expired_user(get_api_client):
    api_client = get_api_client
    await api_client.add_user(
        username=expired_user_username,
        expire=expired_user_expire,
        proxies=user_proxies,
    )
    time.sleep(10)  # Delay between creating expired user and changing its status to expired


async def test_get_expired_users(get_api_client):
    api_client = get_api_client
    expired_users = await api_client.get_expired_users()
    assert expired_user_username in expired_users


async def test_delete_expired_users(get_api_client):
    api_client = get_api_client
    await api_client.delete_expired_users()
    all_users = await api_client.get_users()
    assert expired_user_username not in [user.username for user in all_users.users]


async def test_remove_user(get_api_client):
    api_client = get_api_client
    await api_client.remove_user(username=user_username)
    users = await api_client.get_users()
    assert user_username not in [user.username for user in users.users]
