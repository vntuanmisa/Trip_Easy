from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    database_host: str
    database_port: int = 26083
    database_user: str
    database_password: str
    database_name: str = "tripeasy"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    google_maps_api_key: str = ""
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}?ssl_ca=ca-cert.pem"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
