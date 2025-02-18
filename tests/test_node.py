from tests.conftest import get_api_client


node_name = "Test node"
node_address = "8.8.8.8"
node_usage_coefficient = 0.2
node_add_as_new_host = False
node_id = None


async def test_get_node_settings(get_api_client):
    api_client = get_api_client
    await api_client.get_node_settings()


async def test_add_node(get_api_client):
    api_client = get_api_client
    node = await api_client.add_node(
        name=node_name,
        address=node_address,
        usage_coefficient=node_usage_coefficient,
        add_as_new_host=node_add_as_new_host,
    )
    assert node.name == node_name
    assert node.address == node_address
    # assert node.usage_coefficient == node_usage_coefficient # TODO: Marzban API error: usage_coefficient always = 1 when creating node
    assert node.port == 62050
    assert node.api_port == 62051

    global node_id
    node_id = node.id


async def test_get_node(get_api_client):
    api_client = get_api_client
    node = await api_client.get_node(node_id=node_id)
    assert node.name == node_name
    assert node.address == node_address



new_node_address = "1.1.1.1"
new_usage_coefficient = 0.5
new_node_port = 30000
new_node_api_port = 30001
new_node_name = "New test node"


async def test_modify_node(get_api_client):
    api_client = get_api_client
    node = await api_client.modify_node(
        node_id=node_id,
        name=new_node_name,
        address=new_node_address,
        usage_coefficient=new_usage_coefficient,
        port=new_node_port,
        api_port=new_node_api_port,
    )
    assert node.name == new_node_name
    assert node.address == new_node_address
    assert node.usage_coefficient == new_usage_coefficient
    assert node.port == new_node_port
    assert node.api_port == new_node_api_port


async def test_get_nodes(get_api_client):
    api_client = get_api_client
    nodes = await api_client.get_nodes()
    node_ids = [node.id for node in nodes]
    assert node_id in node_ids


async def test_reconnect_node(get_api_client):
    api_client = get_api_client
    await api_client.reconnect_node(node_id=node_id)


# async def test_get_usage(get_api_client):
#     api_client = get_api_client
#     usages = await api_client.get_node_usage(
#         start="08.02.2025",
#         end="18.02.2025",
#     )


async def test_remove_node(get_api_client):
    api_client = get_api_client
    await api_client.remove_node(node_id=node_id)

    nodes = await api_client.get_nodes()
    node_ids = [node.id for node in nodes]
    assert node_id not in node_ids
