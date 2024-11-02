from fastapi import APIRouter


router = APIRouter(prefix="/hello", tags=["hello-world"])


# PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
# PLAID_SECRET = os.getenv('PLAID_SECRET')
# PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')
# PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')


@router.get("/hello-world")
def hello_world():
    return {"message": "This came from FastAPI"}