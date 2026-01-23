import os

def get_db_type() -> str:
    return os.getenv("DB_TYPE", "postgres").lower()