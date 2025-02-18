from typing import List, Union

from aiomarzban import UserResponse, Admin
from .conftest import get_api_client

admin_username = "admin"
admin_password = "123"
admin_is_sudo = False
admin_telegram_id = 1


def get_usernames(users: Union[List[Admin], List[UserResponse]]) -> List[str]:
    return [user.username for user in users]


async def test_get_current_admin(get_api_client):
    api_client = get_api_client

    current_admin = await api_client.get_current_admin()
    assert current_admin.is_sudo is True


async def test_create_admin(get_api_client):
    api_client = get_api_client

    admin = await api_client.create_admin(
        username=admin_username,
        password=admin_password,
        is_sudo=admin_is_sudo,
        telegram_id=admin_telegram_id,
    )

    assert admin.username == admin_username
    assert admin.is_sudo == admin_is_sudo
    assert admin.telegram_id == admin_telegram_id
    assert admin.discord_webhook is None
    assert admin.users_usage == 0


new_admin_telegram_id = 2


async def test_modify_admin(get_api_client):
    api_client = get_api_client
    admin = await api_client.modify_admin(
        username = admin_username,
        is_sudo = admin_is_sudo,
        telegram_id = new_admin_telegram_id,
    )

    assert admin.username == admin_username
    assert admin.is_sudo == admin_is_sudo
    assert admin.telegram_id == new_admin_telegram_id
    assert admin.discord_webhook is None
    assert admin.users_usage == 0


async def test_get_admins(get_api_client):
    api_client = get_api_client

    admins = await api_client.get_admins()
    assert len(admins) > 0


async def test_disable_all_active_users(get_api_client):
    api_client = get_api_client
    await api_client.disable_all_active_users(username=admin_username)


async def test_activate_all_disabled_users(get_api_client):
    api_client = get_api_client
    await api_client.activate_all_disabled_users(username=admin_username)


async def test_reset_admin_usage(get_api_client):
    api_client = get_api_client
    admin = await api_client.reset_admin_usage(username=admin_username)
    assert admin.users_usage == 0


async def test_get_users_usage(get_api_client):
    api_client = get_api_client
    admin_usage = await api_client.get_admin_usage(username=admin_username)
    assert isinstance(admin_usage, int)


async def test_remove_admin(get_api_client):
    api_client = get_api_client

    await api_client.remove_admin(username=admin_username)
    admins = await api_client.get_admins()
    assert admin_username not in get_usernames(admins)
