import copy
import json
import os
import time

from tests.conftest import get_api_client

original_hosts = None

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "hosts.json"))
with open(file_path) as f:
    new_hosts = json.load(f)


async def test_get_system_stats(get_api_client):
    api_client = get_api_client
    await api_client.get_system_stats()


async def test_get_inbounds(get_api_client):
    api_client = get_api_client
    await api_client.get_inbounds()


async def test_get_hosts(get_api_client):
    api_client = get_api_client
    global original_hosts
    original_hosts = await api_client.get_hosts()


async def test_modify_hosts(get_api_client):
    api_client = get_api_client

    # Creating new modified hosts
    modified_hosts = copy.deepcopy(new_hosts)
    modified_hosts["VLESS host"][0]["remark"] = "Test host modification"

    # Applying modified hosts and checking if it is working
    updated_hosts = await api_client.modify_hosts(modified_hosts)
    assert updated_hosts != new_hosts, "Hosts were not modified."

    # Settings original hosts
    time.sleep(0.5)
    restored_hosts = await api_client.modify_hosts(original_hosts)
    assert restored_hosts == original_hosts, "Hosts were not restored to original."
