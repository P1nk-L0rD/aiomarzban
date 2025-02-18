from aiomarzban import MarzbanAPI


async def delete_all_data(api_client: MarzbanAPI):
    users = await api_client.get_users()
    for user in users.users:
        await api_client.remove_user(user.username)
        print(f"User {user.username} deleted successfully.")

    admins = await api_client.get_admins()
    for admin in [admin for admin in admins if not admin.is_sudo]:
        await api_client.remove_admin(admin.username)
        print(f"User {admin.username} deleted successfully.")

    nodes = await api_client.get_nodes()
    for node in nodes:
        await api_client.remove_node(node.id)
        print(f"Node {node.id} deleted successfully.")

    templates = await api_client.get_user_templates()
    for template in templates:
        await api_client.remove_user_template(template.id)
        print(f"User {template.username} deleted successfully.")
