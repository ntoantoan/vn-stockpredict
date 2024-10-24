import os
import time
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from pydantic import BaseModel

from ..chart.get_chart_from_vndirect import ChartScreenshotCapture
from ..database import Database
from ..services.analyze_chart_stream import analyze_chart_stream

db = Database()

# chart_capture = ChartScreenshotCapture("HPG")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/chart-analysis", tags=["chart-analysis"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Add this rate limiting logic
RATE_LIMIT = 2
RATE_LIMIT_WINDOW = 3600
request_counts = defaultdict(lambda: {"count": 0, "reset_time": 0})


class User(BaseModel):
    username: str
    email: str
    password: str

class ChartAnalysisRequest(BaseModel):
    base64_image: str
    model: str = "gpt-4-0613"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Check token expiration
        exp = payload.get("exp")
        if exp is None:
            raise credentials_exception
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise credentials_exception
    user = db.get_user(username)
    if user is None:
        raise credentials_exception
    return user


def check_rate_limit(ip: str):
    current_time = time.time()
    if current_time > request_counts[ip]["reset_time"]:
        request_counts[ip] = {"count": 1, "reset_time": current_time + RATE_LIMIT_WINDOW}
    else:
        request_counts[ip]["count"] += 1

    if request_counts[ip]["count"] > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@router.post("/analyze-chart")
async def analyze_chart_endpoint(
    request: Request,
    chart_request: ChartAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    client_ip = request.client.host
    check_rate_limit(client_ip)
    
    try:
        return await analyze_chart_stream(chart_request.base64_image, model=chart_request.model, user=current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get-chart/{symbol}")
async def get_chart_endpoint(symbol: str, current_user: User = Depends(get_current_user)):
    chart_capture = ChartScreenshotCapture(symbol)
    base64_image = chart_capture.run(symbol)
    return {"base64_image": base64_image, "user": current_user.username}