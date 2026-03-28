# Remove shims re-exporting from `fastapi_tools`

## Overview

Remove all the shims that re-export from `fastapi_tools` in `python-project-template`
eg `src/project_name/webapp/core/__init__.py`, but many more are present.

---

## Shim files (pure re-export, delete after updating consumers)

### `src/project_name/config/webapp/__init__.py`

Re-exports `CORSConfig`, `GoogleOAuthConfig`, `RateLimitConfig`, `SessionConfig`, `WebappConfig`
from `fastapi_tools.config.webapp_config`.

### `src/project_name/config/webapp/webapp_config.py`

Duplicate of the `__init__.py` shim above - same five symbols, same source, uses `as X` aliases.

### `src/project_name/webapp/core/__init__.py`

Re-exports `get_current_user` from `fastapi_tools.dependencies` and
`NotAuthenticatedException`, `NotAuthorizedException`, `RateLimitExceededException`
from `fastapi_tools.exceptions`.

### `src/project_name/webapp/core/exceptions.py`

Re-exports `NotAuthenticatedException`, `NotAuthorizedException`, `RateLimitExceededException`,
`ServiceUnavailableException`, `ValidationException` from `fastapi_tools.exceptions`.

### `src/project_name/webapp/core/middleware.py`

Re-exports `RequestIDMiddleware`, `RequestLoggingMiddleware`, `SecurityHeadersMiddleware`,
`setup_middleware` from `fastapi_tools.middleware`.

### `src/project_name/webapp/core/security.py`

Re-exports `TokenManager`, `generate_session_id`, `generate_state_token`, `get_expiration_time`,
`hash_token`, `is_expired`, `sanitize_dict`, `sanitize_html` from `fastapi_tools.security`.

### `src/project_name/webapp/core/templating.py`

Re-exports `configure_templates`, `make_templates` from `fastapi_tools.templating`.

### `src/project_name/webapp/routers/auth_router.py`

Re-exports `router` from `fastapi_tools.routers.auth`.

### `src/project_name/webapp/routers/health_router.py`

Re-exports `router` from `fastapi_tools.routers.health`.

### `src/project_name/webapp/schemas/__init__.py`

Re-exports `GoogleUserInfo`, `LoginResponse`, `SessionData`, `UserResponse` from
`fastapi_tools.schemas.auth` and `ErrorResponse`, `HealthResponse` from
`fastapi_tools.schemas.common`.

### `src/project_name/webapp/schemas/auth_schemas.py`

Re-exports `AuthURLResponse`, `GoogleUserInfo`, `LoginResponse`, `LogoutResponse`,
`SessionData`, `UserResponse` from `fastapi_tools.schemas.auth`.

### `src/project_name/webapp/schemas/common_schemas.py`

Re-exports `ErrorResponse`, `HealthResponse`, `MessageResponse`, `PaginatedResponse`,
`PaginationParams`, `ReadinessResponse` from `fastapi_tools.schemas.common`.

### `src/project_name/webapp/services/__init__.py`

Re-exports `GoogleAuthService`, `SessionStore` from `fastapi_tools.auth.google`.

### `src/project_name/webapp/services/auth_service.py`

Re-exports `GoogleAuthService`, `SessionStore` from `fastapi_tools.auth.google`.
Duplicate of the services `__init__.py` shim above.

---

## Hybrid shim (shim re-exports + real code - keep file, strip re-exports)

### `src/project_name/webapp/core/dependencies.py`

Shim re-exports: `get_current_session`, `get_current_user`, `get_db_session`,
`get_optional_user`, `get_session_store` from `fastapi_tools.dependencies`.

Real code that must stay: `get_settings()` function (returns `WebappConfig` from
`get_webapp_params().to_config()`). Its `TYPE_CHECKING` import
`from project_name.config.webapp import WebappConfig` must change to
`from fastapi_tools.config.webapp_config import WebappConfig`.

---

## Consumers and required import changes

### `src/project_name/params/webapp/webapp_params.py`

| Current | Direct |
|---|---|
| `from project_name.config.webapp import CORSConfig` | `from fastapi_tools.config.webapp_config import CORSConfig` |
| `from project_name.config.webapp import GoogleOAuthConfig` | `from fastapi_tools.config.webapp_config import GoogleOAuthConfig` |
| `from project_name.config.webapp import RateLimitConfig` | `from fastapi_tools.config.webapp_config import RateLimitConfig` |
| `from project_name.config.webapp import SessionConfig` | `from fastapi_tools.config.webapp_config import SessionConfig` |
| `from project_name.config.webapp import WebappConfig` | `from fastapi_tools.config.webapp_config import WebappConfig` |

### `src/project_name/webapp/api/v1/api_router.py`

| Current | Direct |
|---|---|
| `from project_name.webapp.core.dependencies import get_current_user` | `from fastapi_tools.dependencies import get_current_user` |
| `from project_name.webapp.schemas.auth_schemas import SessionData` | `from fastapi_tools.schemas.auth import SessionData` |
| `from project_name.webapp.schemas.common_schemas import MessageResponse` | `from fastapi_tools.schemas.common import MessageResponse` |

### `src/project_name/webapp/core/dependencies.py` (TYPE_CHECKING block only)

| Current | Direct |
|---|---|
| `from project_name.config.webapp import WebappConfig` | `from fastapi_tools.config.webapp_config import WebappConfig` |

### `tests/config/webapp/__init__.py`

| Current | Direct |
|---|---|
| `from project_name.config.webapp import CORSConfig` | `from fastapi_tools.config.webapp_config import CORSConfig` |
| `from project_name.config.webapp import GoogleOAuthConfig` | `from fastapi_tools.config.webapp_config import GoogleOAuthConfig` |
| `from project_name.config.webapp import RateLimitConfig` | `from fastapi_tools.config.webapp_config import RateLimitConfig` |
| `from project_name.config.webapp import SessionConfig` | `from fastapi_tools.config.webapp_config import SessionConfig` |
| `from project_name.config.webapp import WebappConfig` | `from fastapi_tools.config.webapp_config import WebappConfig` |

### `tests/webapp/conftest.py`

| Current | Direct |
|---|---|
| `from project_name.config.webapp import CORSConfig` | `from fastapi_tools.config.webapp_config import CORSConfig` |
| `from project_name.config.webapp import GoogleOAuthConfig` | `from fastapi_tools.config.webapp_config import GoogleOAuthConfig` |
| `from project_name.config.webapp import RateLimitConfig` | `from fastapi_tools.config.webapp_config import RateLimitConfig` |
| `from project_name.config.webapp import SessionConfig` | `from fastapi_tools.config.webapp_config import SessionConfig` |
| `from project_name.config.webapp import WebappConfig` | `from fastapi_tools.config.webapp_config import WebappConfig` |
| `from project_name.webapp.schemas.auth_schemas import GoogleUserInfo` | `from fastapi_tools.schemas.auth import GoogleUserInfo` |
| `from project_name.webapp.schemas.auth_schemas import SessionData` | `from fastapi_tools.schemas.auth import SessionData` |

### `tests/webapp/test_auth.py`

| Current | Direct |
|---|---|
| `from project_name.webapp.schemas.auth_schemas import SessionData` | `from fastapi_tools.schemas.auth import SessionData` |

### `tests/webapp/test_pages.py`

| Current | Direct |
|---|---|
| `from project_name.webapp.schemas.auth_schemas import SessionData` | `from fastapi_tools.schemas.auth import SessionData` |

---

## Already importing directly from `fastapi_tools` (no change needed)

- `src/project_name/webapp/main.py` - `from fastapi_tools import create_app`
- `src/project_name/webapp/routers/pages_router.py` - imports directly from
  `fastapi_tools.dependencies` and `fastapi_tools.schemas.auth`
- `tests/webapp/conftest.py` - `from fastapi_tools import create_app` (already direct)

---

## Execution order

1. Update all consumers (files listed above) to import directly from `fastapi_tools`.
2. Strip the shim re-exports from `src/project_name/webapp/core/dependencies.py`
   (keep `get_settings()`).
3. Delete the 14 pure-shim files.
4. Run `uv run pytest && uv run ruff check . && uv run pyright` to verify.

## Linting check

in `ruff.toml` an exception for

```
    "PLC0414", # Import alias does not rename original package (re-export shims)
```

was added. After the shims are removed, this exception can be deleted and any remaining `PLC0414` issues should be resolved by renaming the import alias to match the original package name.
