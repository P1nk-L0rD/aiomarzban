from aiomarzban.utils import gb_to_bytes
from tests.conftest import get_api_client

user_template_name = "Test user template"
user_template_data_limit = 100
user_template_expire_duration = 60 * 60 * 24
user_template_username_prefix = "prefix"
user_template_username_suffix = "suffix"
user_template_inbounds = {}


user_template_id = None


async def test_add_user_template(get_api_client):
    api_client = get_api_client
    user_template = await api_client.add_user_template(
        name=user_template_name,
        data_limit=user_template_data_limit,
        expire_duration=user_template_expire_duration,
        username_prefix=user_template_username_prefix,
        username_suffix=user_template_username_suffix,
        inbounds=user_template_inbounds,
    )

    assert user_template.name == user_template_name
    assert user_template.data_limit == gb_to_bytes(user_template_data_limit)
    assert user_template.expire_duration == user_template_expire_duration
    assert user_template.username_prefix == user_template_username_prefix
    assert user_template.username_suffix == user_template_username_suffix
    assert user_template_inbounds == user_template_inbounds

    global user_template_id
    user_template_id = user_template.id


async def test_get_user_templates(get_api_client):
    api_client = get_api_client
    user_templates = await api_client.get_user_templates()
    assert user_template_id in [user_template.id for user_template in user_templates]


async def test_get_user_template(get_api_client):
    api_client = get_api_client
    user_template = await api_client.get_user_template(user_template_id)
    assert user_template.id == user_template_id
    assert user_template.name == user_template_name
    assert user_template.data_limit == gb_to_bytes(user_template_data_limit)


new_user_template_name = "Test new user template"
new_user_template_data_limit = 20
new_user_template_expire_duration = 60 * 60 * 2
new_user_template_username_prefix = "new_prefix"
new_user_template_username_suffix = "new_suffix"


async def test_modify_user_template(get_api_client):
    api_client = get_api_client
    new_user_template = await api_client.modify_user_template(
        template_id=user_template_id,
        name=new_user_template_name,
        data_limit=new_user_template_data_limit,
        expire_duration=new_user_template_expire_duration,
        username_prefix=new_user_template_username_prefix,
        username_suffix=new_user_template_username_suffix,
    )

    assert new_user_template.id == user_template_id
    assert new_user_template.name == new_user_template_name
    assert new_user_template.data_limit == gb_to_bytes(new_user_template_data_limit)
    assert new_user_template.expire_duration == new_user_template_expire_duration
    assert new_user_template.username_prefix == new_user_template_username_prefix
    assert new_user_template.username_suffix == new_user_template_username_suffix


second_user_template_expire_duration = 60 * 60 * 8


async def test_modify_user_template_one_field(get_api_client):
    api_client = get_api_client
    new_user_template = await api_client.modify_user_template(
        template_id=user_template_id,
        expire_duration=second_user_template_expire_duration,
    )
    assert new_user_template.expire_duration == second_user_template_expire_duration


async def test_remove_user_template(get_api_client):
    api_client = get_api_client
    await api_client.remove_user_template(user_template_id)
    user_templates = await api_client.get_user_templates()
    assert user_template_id not in [user_template.id for user_template in user_templates]
