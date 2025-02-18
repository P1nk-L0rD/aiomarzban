import copy
import json
import os
import time

from tests.conftest import get_api_client

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cfg.json"))
with open(file_path) as f:
    new_cfg = json.load(f)


async def test_get_core_stats(get_api_client):
    api_client = get_api_client
    await api_client.get_core_stats()


async def test_get_core_config(get_api_client):
    api_client = get_api_client
    await api_client.get_core_config()


async def test_modify_core_config(get_api_client):
    api_client = get_api_client
    old_cfg = await api_client.get_core_config()

    # Setting first config
    example_cfg = copy.deepcopy(new_cfg)
    example_cfg["inbounds"][0]["port"] = 11111
    panel_cfg = await api_client.modify_core_config(example_cfg)
    assert panel_cfg != new_cfg, "Old and new core configs are the same."

    # Settings second config and comparing
    time.sleep(0.5)
    await api_client.modify_core_config(new_cfg)
    current_cfg = await api_client.get_core_config()
    assert current_cfg == new_cfg, "The new config was not installed."

    # Returning old config
    time.sleep(0.5)
    await api_client.modify_core_config(old_cfg)


async def test_restart_core(get_api_client):
    api_client = get_api_client
    await api_client.restart_core()
