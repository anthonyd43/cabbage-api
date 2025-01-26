from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date


class Location(BaseModel):
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    lat: str
    lon: str
    store_number: str


class CounterParty(BaseModel):
    name: str
    type: str
    website: Optional[str]
    logo_url: Optional[str]
    confidence_level: str
    entity_id: str
    phone_number: Optional[str]


class Transaction(BaseModel):
    account_id: str
    account_owner: Optional[str]
    amount: Decimal
    authorized_date: date
    categories: List[str]
    category_id: str
    counter_parties: List[CounterParty]
    iso_currency_code: str
    location: Optional[Location]
    merchant_entity_id: str
    merchant_name: str
    payment_channel: str 
    pending: bool