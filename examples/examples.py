from aiomarzban import MarzbanAPI

marzban = MarzbanAPI(
    address="https://my_domain.com/",
    username="admin",
    password="super_secret_password",
)

async def main():
    # Admins
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

    # TODO: write other examples
