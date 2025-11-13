import os
from typing import Literal

def get_db_type() -> str:
    return os.getenv("DB_TYPE", "postgres").lower()