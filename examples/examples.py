from aiomarzban import MarzbanAPI


marzban = MarzbanAPI(
    address="https://my_domain.com/",
    username="admin",
    password="super_secret_password",
)


async def main():

    # Admin

    # Get current admin
    current_admin = await marzban.get_current_admin()
    print("Current admin: ", current_admin)

    # Create admin
    new_admin = await marzban.create_admin(username="new_admin", password="12345678")
    print("New admin: ", new_admin)

    # Modify admin
    modified_admin = await marzban.modify_admin(username="new_admin", telegram_id=123456, is_sudo=False)
    print("Modified admin: ", modified_admin)

    # Remove admin
    await marzban.remove_admin("new_admin")
    print("'new_admin' has been removed")

    # Get admins
    admins = marzban.get_admins(offset=0, limit=10)
    print("Admins: ", admins)

    # Disable all active users of admin
    response = await marzban.disable_all_active_users("new_admin")
    print(response)

    # Activate all disabled users of admin
    response = await marzban.activate_all_disabled_users("new_admin")
    print(response)

    # Reset usage of users created by specific admin
    admin = await marzban.reset_admin_usage("new_admin")
    print("Admin: ", admin)

    # Get usage of users created by specific admin
    usage = await marzban.get_admin_usage("new_admin")
    print("Usage: ", usage)

    # Core

    # Get core stats
    core_stats = await marzban.get_core_stats()
    print("Core stats: ", core_stats)

    # Restart core
    await marzban.restart_core()
    print("Core restarted")

    core_config = await marzban.get_core_config()
    print("Core config: ", core_config)

    modified_core_config = await marzban.modify_core_config(core_config)
    print("Modified core config: ", modified_core_config)

    # Node
    # Get node settings
    node_settings = await marzban.get_node_settings()
    print("Node settings: ", node_settings)

    # Add new node
    new_node = await marzban.add_node(name="new_node", address="8.8.8.8")
    print("New node: ", new_node)

    # Get node
    node = await marzban.get_node(new_node.id)
    print("Node: ", node)

    # Modify node
    modified_node = await marzban.modify_node(new_node.id, address="1.1.1.1")
    print("Modified node: ", modified_node)

    # Remove node
    await marzban.remove_node(new_node.id)
    print("Removed node: ", new_node)

    # Get nodes
    nodes = await marzban.get_nodes()
    print("Nodes: ", nodes)

    # Reconnect node
    await marzban.reconnect_node(new_node.id)
    print("Reconnected node: ", new_node)

    node_usage = await marzban.get_nodes_usage()
    print("Node usage: ", node_usage)

    # Subscription

    # TODO: write examples

    # System

    # Get system stats
    system_stats = await marzban.get_system_stats()
    print("System stats: ", system_stats)

    # Get inbounds
    inbounds = await marzban.get_inbounds()
    print("Inbounds: ", inbounds)

    # Get hosts
    hosts = await marzban.get_hosts()
    print("Hosts: ", hosts)

    # Modify hosts
    new_hosts = await marzban.modify_hosts(hosts)
    print("New hosts: ", new_hosts)

    # User template

    # Add user template
    user_template = await marzban.add_user_template(name="Test")
    print("User template: ", user_template)

    # Get user templates
    user_templates = await marzban.get_user_templates()
    print("User templates: ", user_templates)

    # Get user template
    user_template = await marzban.get_user_template(user_template.id)
    print("User template: ", user_template)

    # Modify user template
    modified_user_template = await marzban.modify_user_template(user_template.id, data_limit=100)
    print("Modified user template: ", modified_user_template)

    # Remove user template
    await marzban.remove_user_template(user_template.id)
    print("Removed user template: ", user_template)

    # User

    # Add user
    user = await marzban.add_user(username="test_user", data_limit=10, days=8)
    print("User: ", user)

    # Get user
    user = await marzban.get_user(user.username)
    print("User: ", user)

    # Modify user
    modified_user = await marzban.modify_user(user.username, data_limit=100, note="test_note")
    print("Modified user: ", modified_user)

    # Remove user
    await marzban.remove_user(user.username)
    print("Removed user: ", user)

    # Reset user usage data
    user = await marzban.reset_user_usage_data(user.username)
    print("User: ", user)

    # Revoke user subscription
    revoked_user = await marzban.revoke_user_subscription(user.username)
    print("Revoked user: ", revoked_user)

    # Get users
    users = await marzban.get_users(offset=0, limit=10)
    print("Users: ", users)

    # Reset all users usage data
    resp = await marzban.reset_users_usage_data()
    print("Users usage data reset: ", resp)

    # Get user usage
    user_usage = await marzban.get_user_usage(user.username)
    print("User usage: ", user_usage)

    # Active next plan
    modified_user = await marzban.active_next_plan(user.username)
    print("Modified user: ", modified_user)

    # Get users usage
    users_usage = await marzban.get_users_usage()
    print("Users usage: ", users_usage)

    # Set owner (Not working in Marzban API 0.8.4)
    modified_user = await marzban.set_owner(user.username, admin_username=current_admin.username)
    print("Modified user: ", modified_user)

    # Get expired users
    expired_users = await marzban.get_expired_users()
    print("Expired users: ", expired_users)

    # Delete expired users
    deleted_users = await marzban.delete_expired_users()
    print("Deleted users: ", deleted_users)

    # Extra methods

    # Add days to user subscription
    modified_user = await marzban.user_add_days(user.username, days=7)
    print("Modified user: ", modified_user)

    # Allow all inbounds
    modified_user = await marzban.user_set_all_inbounds(modified_user)
    print("Modified user: ", modified_user)
