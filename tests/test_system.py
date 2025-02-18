import copy
import json
import os
import time

from tests.conftest import get_api_client

hosts = None

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
    global hosts
    hosts = await api_client.get_hosts()


async def test_modify_hosts(get_api_client):
    api_client = get_api_client

    first_hosts = copy.deepcopy(new_hosts)
    first_hosts["VLESS host"][0]["remark"] = "First test host"
    current_hosts = await api_client.modify_hosts(first_hosts)
    assert current_hosts != new_hosts, "Hosts were not modified."

    # Settings second config and comparing
    time.sleep(0.5)
    current_hosts = await api_client.modify_hosts(new_hosts)
    assert current_hosts == new_hosts, "Hosts were not modified."

    # Setting old hosts
    time.sleep(0.5)
    await api_client.modify_hosts(hosts)
