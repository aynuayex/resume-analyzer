import os
import shutil

import requests
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Header
from jose import jwt, JWTError

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


@router.post("/upload")
def upload(file: UploadFile = File(...), user=Depends(verify_token)):
    filepath = f"/tmp/{file.filename}"
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    res = requests.post(
        N8N_WEBHOOK_URL, json={"file_path": filepath, "filename": file.filename}
    )
    return {"message": "Uploaded and sent to n8n", "n8n_response": res.status_code}