from __future__ import annotations

import datetime as dt
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from .aggregator import InvoiceItem
from .config import OUTPUT_DIR, TEMPLATE_FILE


class InvoiceRenderer:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(str(TEMPLATE_FILE.parent)))
        self.template = self.env.get_template(TEMPLATE_FILE.name)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def render_invoices(self, items: Iterable[InvoiceItem]):
        for item in items:
            context = asdict(item)
            html = self.template.render(**context)
            file_name = f"{item.property}-{item.month}.pdf"
            output_file = OUTPUT_DIR / file_name
            HTML(string=html).write_pdf(output_file)
            print(f"Generated {output_file}")
