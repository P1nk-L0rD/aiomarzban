import pytest

from .conftest import MarzbanAPI

admin_username = "admin"
admin_password = "123"
admin_is_sudo = False
admin_telegram_id = 1



@pytest.mark.asyncio
async def test_create_admin(api_client: MarzbanAPI):
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


new_admin_username = "admin2"
new_admin_password = "1234"
new_admin_telegram_id = 2


@pytest.mark.asyncio
async def test_modify_admin(api_client: MarzbanAPI):
    admin = await api_client.modify_admin(
        username = new_admin_username,
        is_sudo = False,
    )

    assert admin.username == new_admin_username
    assert admin.is_sudo == admin_is_sudo
    assert admin.telegram_id == admin_telegram_id
    assert admin.discord_webhook is None
    assert admin.users_usage == 0





