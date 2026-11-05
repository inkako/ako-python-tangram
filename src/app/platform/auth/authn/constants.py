# ===========================================
# time units
# ===========================================
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR


# ===========================================
# Storage / storage
# ===========================================
# Root session storage key namespace prefix.
SESSION_STORAGE_PREFIX = "session:"
# Suffix appended to the prefix root for the per-user session index (redis).
USER_INDEX_SUFFIX = "users:"
# CSRF storage namespace prefix
CSRF_STORAGE_PREFIX = "csrf:"

CSRF_TOKEN_BYTES = 32

USER_INDEX_TTL_BUFFER_SECONDS = SECONDS_PER_HOUR

# Session-metadata keys.
REMEMBER_ME_META_KEY = "remember_me"
CSRF_TOKEN_ID_META_KEY = "csrf_token_id"


# ===========================================
# cookie/header names
# ===========================================
SESSION_COOKIE_NAME = "session_id"
CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"