from pydantic import BaseModel

class Token(BaseModel):
    public_token:str