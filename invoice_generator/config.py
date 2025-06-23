import os
from pathlib import Path
from typing import Optional

import yaml

CONFIG_DIR = Path(os.getenv("AI_INV_CONFIG_DIR", Path.cwd()))
RATE_FILE = CONFIG_DIR / "rates.yaml"
SERVICE_ACCOUNT_FILE = CONFIG_DIR / "service_account.json"
TEMPLATE_FILE = CONFIG_DIR / "invoice_template.html"
OUTPUT_DIR = CONFIG_DIR / "invoices"


class Config:
    def __init__(self):
        self.rate_table = self.load_rates()

    def load_rates(self) -> dict:
        if RATE_FILE.exists():
            with open(RATE_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}


config = Config()
