import time
import logging
from datetime import date, timedelta
import plaid
from config import PlaidConfig
from models.plaid_model import PublicToken
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse
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
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.transactions_sync_request import TransactionsSyncRequest

load_dotenv()

# Setup Logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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
            country_codes=list(
                map(lambda x: CountryCode(x), plaid_config.COUNTRY_CODES)
            ),
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
        logging.info(response)
        return response.to_dict()
    except Exception as ex:
        return {"error": ex}


# Gets the access token from the public token
@router.post("/exchange_public_token")
async def exchange_public_token(Token: PublicToken):
    global access_token
    global item_id
    logging.info(f"Exchanging public token with Plaid")
    try:
        public_token = Token.public_token
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]

        logging.info(f"Public Token has been Exchanged")
        return JSONResponse(content={"message": "Success"}, status_code=200)

    except Exception as ex:
        return {"error": ex}

@router.post("/transactions")
async def get_transactions():
    cursor = ""

    # New transaction updates since "cursor"
    added = []
    modified = []
    removed = []  # Removed transaction ids
    has_more = True
    try:
        # Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=cursor,
            )
            response = client.transactions_sync(request).to_dict()
            cursor = response["next_cursor"]
            if cursor == "":
                time.sleep(2)
                continue
            # If cursor is not an empty string, we got results,
            # so add this page of results
            added.extend(response["added"])
            modified.extend(response["modified"])
            removed.extend(response["removed"])
            has_more = response["has_more"]
        # Return the 8 most recent transactions
        latest_transactions = sorted(added, key=lambda t: t["date"])[-8:]
        print(f"Latest Trans: {latest_transactions}")
        # return JSONResponse(latest_transactions)
        return JSONResponse(content={"message": "Success"}, status_code=200)

    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(content=error_response, status_code=400)


def format_error(e):
    response = e.response.json()
    return {
        "error": {
            "status_code": response["status_code"],
            "error_code": response["error_code"],
            "error_message": response["error_message"],
            "display_message": response["display_message"],
            "request_id": response["request_id"],
            "causes": response["causes"],
            "documentation_url": response["documentation_url"],
            "suggested_action": response["suggested_action"],
        }
    }
