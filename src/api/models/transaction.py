from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    account_id: str = Field(..., description="Identifier linking the transaction to a specific account")
    name: str = Field(..., description="Transaction name or merchant descriptor")
    amount: float = Field(..., description="Transaction amount in the account's currency")
    posted_date: date = Field(..., description="Date the transaction was posted")
    iso_currency_code: Optional[str] = Field(None, description="3-letter ISO currency code, e.g. USD")
    category: Optional[List[str]] = Field(None, description="List of category labels from Plaid or custom tags")
    category_id: Optional[str] = Field(None, description="Plaid category ID or custom category reference")
    pending: bool = Field(False, description="Indicates if the transaction is still pending")
    payment_channel: Optional[str] = Field(None, description="e.g., 'online', 'in store'")
    transaction_type: Optional[str] = Field(None, description="e.g., 'place', 'digital', 'special'")
    merchant_name: Optional[str] = Field(None, description="Merchant or payee name, if available")

