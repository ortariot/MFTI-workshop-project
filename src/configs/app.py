from dynaconf import Dynaconf
from pydantic import BaseModel


class APPConfig(BaseModel):
    app_version: str
    app_name: str
    app_host: str
    app_port: int


class DBConfig(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    @property
    def dsl(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # driver://user:password@host:port/db_name


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int



class Cache(BaseModel):
    cache_port: int
    cache_host: str

class Settings(BaseModel):
    app: APPConfig
    db: DBConfig
    auth: AuthConfig
    cache: Cache


env_settings = Dynaconf(
    envvar_prefix="DOCKER",
    load_dotenv=True,
    settings_file=["settings.toml"]
    )

settings = Settings(
    app=env_settings["app_settings"],
    db=env_settings["db_settings"],
    auth=env_settings["auth_settings"],
    cache=env_settings["cache_settings"],
)


if __name__ == "__main__":
    print(settings)
