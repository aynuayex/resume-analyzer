import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from fastapi import FastAPI
from auth import router as auth_router
from upload import router as upload_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(upload_router)
