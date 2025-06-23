# AI Invoice Generator

This tool generates monthly invoices from Google Calendar events.

## Requirements

- Python 3.8+
- `weasyprint`, `jinja2`, `google-api-python-client`, `google-auth`

Install dependencies with:

```bash
pip install weasyprint jinja2 google-api-python-client google-auth
```

## Configuration

Create a `config/` directory with:

- `rates.yaml` – mapping of property names to hourly rates.
- `service_account.json` – Google service account credentials with Calendar read access.
- `invoice_template.html` – HTML template for invoices.

Set `AI_INV_CONFIG_DIR` environment variable to point to this directory if different.

## Usage

```bash
python -m invoice_generator.cli <calendar_id> <YYYY-MM>
```

PDF invoices will be written to `config/invoices/`.
