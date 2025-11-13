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


class Settings(BaseModel):
    app: APPConfig
    db: DBConfig


env_settings = Dynaconf(settings_file=["settings.toml"])

settings = Settings(app=env_settings["app_settings"], db=env_settings["db_settings"])


if __name__ == "__main__":
    print(settings.db.dsl)
