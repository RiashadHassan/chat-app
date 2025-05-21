SERVER_PERMISSIONS = [
    "can_manage_server",
    "can_edit_server",
    "can_delete_server",
    "can_manage_roles",
    "can_manage_emojis",
    "can_manage_webhooks",
    "can_manage_invites",
    "can_manage_bans",
    "can_view_audit_log",
    "can_change_server_icon",
    "can_change_server_banner",
    "can_change_server_settings",
]

CHANNEL_PERMISSIONS = [
    # Channel Management
    "can_view_channels",
    "can_manage_channels",
    "can_create_channels",
    "can_edit_channels",
    "can_delete_channels",
    "can_move_channels",
    # Channel Participation
    "can_send_messages",
    "can_send_messages_in_threads",
    "can_send_tts_messages",
    "can_embed_links",
    "can_attach_files",
    "can_mention_everyone",
    "can_use_external_emojis",
    "can_use_application_commands",
    "can_create_threads",
    "can_moderate_threads",
    # Message Management
    "can_read_message_history",
    "can_manage_messages",
    "can_pin_messages",
    "can_delete_messages",
    "can_react_to_messages",
    # Voice Permissions
    "can_connect_to_voice",
    "can_speak_in_voice",
    "can_mute_members",
    "can_deafen_members",
    "can_move_members",
    "can_use_voice_activity",
    "can_priority_speak",
]

MEMBER_PERMISSIONS = [
    "can_kick_members",
    "can_ban_members",
    "can_unban_members",
    "can_invite_members",
    "can_manage_nicknames",
    "can_change_own_nickname",
    "can_manage_member_roles",
    "can_assign_roles",
    "can_remove_roles",
    "can_grant_admin",
]

CATEGORY_PERMISSIONS = [
    "can_create_categories",
    "can_edit_categories",
    "can_delete_categories",
]

THREAD_PERMISSIONS = [
    "can_create_threads",
    "can_join_threads",
    "can_archive_threads",
    "can_unarchive_threads",
    "can_delete_threads",
]

ADMIN_PERMISSIONS = [
    "can_view_analytics",
    "can_view_server_insights",
    "can_execute_admin_commands",
    "can_shutdown_server",
    "can_export_data",
    "can_impersonate_users",
    "can_override_permissions",
    "is_admin",
]

EXPERIMENTAL_PERMISSIONS = [
    "can_use_ai_features",
    "can_enable_beta_features",
    "can_edit_permission_overrides",
]

# Final flat list
PERMISSIONS = (
    SERVER_PERMISSIONS
    + CHANNEL_PERMISSIONS
    + MEMBER_PERMISSIONS
    + CATEGORY_PERMISSIONS
    + THREAD_PERMISSIONS
    + ADMIN_PERMISSIONS
    + EXPERIMENTAL_PERMISSIONS
)
