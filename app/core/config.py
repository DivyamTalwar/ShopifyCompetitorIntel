from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FIRECRRAWL_API_KEY: str
    GEMINI_API_KEY: str
    GOOGLE_CSE_ID: str
    GOOGLE_API_KEY: str
    PINECONE_API_KEY: str
    COHERE_API_KEY: str
    PINECONE_INDEX_NAME: str = "shopify-insights"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
