from typing import Optional

from aiomarzban.models import NodeCreate


def add_node(
    name: str,
    address: str,
    port: Optional[int] = None,
    api_port: Optional[int] = None,
    usage_coefficient: Optional[float] = None,
    add_as_new_host: Optional[bool] = None,
) -> NodeCreate:
    data = NodeCreate(
        name=name,
        address=address,
        port=port,
        api_port=api_port,
        usage_coefficient=usage_coefficient,
        add_as_new_host=add_as_new_host,
    )
    print(data.model_dump(exclude_none=True))
    return data

add_node(name="test", address="127.0.0.1", port=12)
