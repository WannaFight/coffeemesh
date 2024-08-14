from fastapi import FastAPI


app = FastAPI(debug=True)

# We import thr api module so that our views can be registred at load time.
from orders.api import api
