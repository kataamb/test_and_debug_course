import json
import logging
import logging.config
import os
from pathlib import Path

config_path = Path(__file__).parent.parent / "log_config.json"

with open(config_path, "r", encoding="utf-8") as f:
    log_config = json.load(f)

logging.config.dictConfig(log_config)
logger = logging.getLogger("app")
logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))
