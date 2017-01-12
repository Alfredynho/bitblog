# -*- encoding:utf-8 -*-

# GENERAL CODES

INTERNAL_SERVER_ERROR = "internal_server_error"
VALIDATION_ERROR = "validation_error"
NOT_FOUND = "not_found"
PERMISSION_DENIED = "permission_denied"
AUTHORIZATION_ERROR = "authorization_error"

# VALIDATION ERROR CODES
INVALID_APPLICATION = "invalid_application"
INVALID_CREDENTIALS = "invalid_credentials"
INVALID_REFRESH_TOKEN = "invalid_refresh_token"
INVALID_ACCESS_TOKEN = "invalid_access_token"
INVALID_TRANSACTION_TOKEN = "invalid_token"
INVALID_ACTION = "invalid_action"
INVALID_EMAIL = "invalid_email"
INVALID_PASSWORD = "invalid_password"
INVALID_SERVICE_CREDENTIALS = "invalid_service_credentials"
UNSUPPORTED_CONTENT_TYPE = "unsupported_content_type"
PASSWORDS_ARENOT_MISMATCH = "passwords_arenot_mismatch"

INACTIVE_ACCOUNT = "inactive_account"
USED_EMAIL = "used_email"
USED_USERNAME = "used_username"

MALFORMED_SUBSCRIPTION = "malformed_subscription"

SUBSCRIPTION_DOES_NOT_MATCH_SERVICE = "subscription_does_not_match_service"
CARD_AND_TOKEN_DO_NOT_MATCH = "card_and_token_do_not_match"
SUBSCRIPTION_AND_TOKEN_DO_NOT_MATCH = "subscription_and_token_do_not_match"

# NOT FOUND ERROR CODES
USER_NOT_FOUND = "user_not_found"
SERVICE_NOT_FOUND = "service_not_found"

# TRANSACTION ERRORS
REGISTERED_SERVICE = "service_registered"
REGISTERED_CARD = "registered_card"
REGISTERED_USER = "registered_user"

# --------------------------------------------
# SUCCESS CODES

ACCOUNT_IS_ACTIVATED = "account_is_activated"
PASSWORD_RESTORED = "password_restored"
EMAIL_UPDATED = "email_updated"
ACCOUNT_DISABLED = "account_disabled"
PASSWORD_CHANGED = "password_changed"
CANCEL_ACCOUNT_SENT = "cancel_account_sent"
SESSIONS_CLEARED = "sessions_cleared"
SUCCESS_LOGOUT = "success_logout"
