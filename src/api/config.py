import os

import plaid
from plaid.model.products import Products
from dotenv import load_dotenv

load_dotenv()


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value


class PlaidConfig:
    CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
    SECRET = os.getenv("PLAID_SECRET")
    ENV = os.getenv("PLAID_ENV", "sandbox")
    PLAID_PRODUCTS = os.getenv("PLAID_PRODUCTS", "transactions").split(",")
    COUNTRY_CODES = os.getenv("PLAID_COUNTRY_CODES", "US").split(",")
    REDIRECT_URI = empty_to_none(os.getenv("PLAID_REDIRECT_URI"))

    host = plaid.Environment.Sandbox
    if ENV == "sandbox":
        host = plaid.Environment.Sandbox
    if ENV == "production":
        host = plaid.Environment.Production

    products = []
    for product in PLAID_PRODUCTS:
        products.append(Products(product))
