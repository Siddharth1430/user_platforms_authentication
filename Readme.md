Database:
Admin -> (
    admin_id(Primary_key),
    admin_name,
    created_platfroms(Foreign_key to Platform(platform_id))
)

User -> (
    user_id(Primary_key),
    user_name,
    joined_platforms(Foreign_key to Platform(platform_id))
)

Platform -> (
    platform_id(Primary_key),
    platform_name,
    Admin(Foreign_key to Admin(admin_id)),
    Users(Foreign_key to User(user_id)),
    Credentials(Foreign_key to Credential(credential_id))
)

Credential -> (
    credential_id(Primary_key),
    username,
    password,
    email(Optional)
)