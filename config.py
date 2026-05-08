from  pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_deployemt_name: str
    azure_openai_api_version: str = ""

    class Config:
        env_file = "env"



settings = Settings()   