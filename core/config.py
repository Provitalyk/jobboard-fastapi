from starlette.config import Config


config = Config(".env_dev")

DATABASE_URL = config("DATABASE_URL", cast=str, default="sqlite:///./employment_exchange")