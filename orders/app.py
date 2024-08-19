from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI(
    debug=True,
    openapi_url="/openapi/orders.json",
    docs_url="/docs/orders",
)

oas_doc = yaml.safe_load(
    (Path(__file__).parent / "../oas.yml").read_text(),
)

app.openapi = lambda: oas_doc

# We import thr api module so that our views can be registred at load time.
from orders.api import api
