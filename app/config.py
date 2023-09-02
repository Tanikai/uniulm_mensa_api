from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    matomo_enabled: bool = False
    matomo_url: str | None = None
    matomo_site_id: int | None = None
