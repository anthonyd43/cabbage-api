from pydantic import BaseModel

class PublicToken(BaseModel):
    public_token:str

    
class AccessToken(BaseModel):
    access_token:str