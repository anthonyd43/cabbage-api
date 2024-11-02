import uvicorn
from api_settings import app

if __name__ == "__main__":
    
    uvicorn.run("__main__:app", port=8000, reload=True)
