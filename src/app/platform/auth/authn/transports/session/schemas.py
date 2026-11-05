from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.platform.util import utcnow


class SessionData(BaseModel):
    user_id: str
    session_id_raw: str = "Unset"
    ip_addr: str = ""
    user_agent: str = ""
    device_info: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utcnow)
    last_activity: datetime = Field(default_factory=utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
    token_version: int | None = None


class UserAgentInfo(BaseModel):
    browser: str = "Unknown"
    browser_version: str = ""
    os: str = "Unknown"
    device: str = "Unknown"
    is_mobile: bool = False
    is_tablet: bool = False
    is_pc: bool = False


class CSRFToken(BaseModel):
    token: str
    session_id: str
    expiry: datetime