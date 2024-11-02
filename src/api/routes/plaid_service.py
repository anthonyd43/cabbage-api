import os
import time
from datetime import date, timedelta

import plaid
from config import PlaidConfig
from models.plaid_model import Token
from dotenv import load_dotenv
from fastapi import APIRouter
from plaid.api import plaid_api
from plaid.model.consumer_report_permissible_purpose import (
    ConsumerReportPermissiblePurpose,
)
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_cra_options import (
    LinkTokenCreateRequestCraOptions,
)
from plaid.model.link_token_create_request_statements import (
    LinkTokenCreateRequestStatements,
)
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
load_dotenv()

router = APIRouter(prefix="/api/plaid", tags=["plaid"])
plaid_config = PlaidConfig()
configuration = plaid.Configuration(
    host=plaid_config.host,
    api_key={
        "clientId": plaid_config.CLIENT_ID,
        "secret": plaid_config.SECRET,
        "plaidVersion": "2020-09-14",
    },
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

access_token = None
payment_id = None
transfer_id = None
user_token = None
item_id = None


@router.post("/create_link_token")
async def create_link_token():
    global user_token
    try:
        request = LinkTokenCreateRequest(
            products=plaid_config.products,
            client_name="Plaid Quickstart",
            country_codes=list(map(lambda x: CountryCode(x), plaid_config.COUNTRY_CODES)),
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=str(time.time())),
        )
        if plaid_config.REDIRECT_URI is not None:
            request["redirect_uri"] = plaid_config.REDIRECT_URI
        if Products("statements") in plaid_config.products:
            statements = LinkTokenCreateRequestStatements(
                end_date=date.today(), start_date=date.today() - timedelta(days=30)
            )
            request["statements"] = statements

        cra_products = [
            "cra_base_report",
            "cra_income_insights",
            "cra_partner_insights",
        ]
        if any(product in cra_products for product in plaid_config.products):
            request["user_token"] = user_token
            request["consumer_report_permissible_purpose"] = (
                ConsumerReportPermissiblePurpose("ACCOUNT_REVIEW_CREDIT")
            )
            request["cra_options"] = LinkTokenCreateRequestCraOptions(days_requested=60)
        # create link token
        response = client.link_token_create(request)
        return response.to_dict()
    except Exception as ex:
        return {"error": ex}

@router.post("/exchange_public_token")
async def exchange_public_token(Token: Token):
    global access_token
    global item_id
    try:
        exchange_request = ItemPublicTokenExchangeRequest(public_token=Token["public_token"])
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]
        return exchange_response.to_dict()
    except Exception as ex:
        return {"error": ex}