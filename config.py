from pydantic import BaseSettings

client = None


class Environment(BaseSettings):
    ES_USER: str
    ES_PASSWORD: str
    ES_URL: str
    # HTTP_CA_CERTIFICATE_PATH: str
    CSV_FILE_PATH: str
    ES_INDEX: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
