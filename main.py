from sqlalchemy.orm import Session
from sqlalchemy import text
from ipaddress import ip_address
from src.database.db import get_db
from src.routes import contacts, auth, users
from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
import redis.asyncio as redis
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, like database connections or caches.
    
    :return: A coroutine
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500', 'http://localhost:5500'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]


@app.get("/")
async def root():
    """
    The root function returns a JSON object with the message &quot;Hello World&quot;.
    
    :return: A dict, which is automatically converted to json
    :doc-author: Trelent
    """
    return {"message": "Hello World"}


# ми перевіряємо що наш застосунок нормально піднявся
@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is used to check the health of the application.
    It can be used by external services such as Kubernetes to determine whether or not this service should be running.
    
    :param db: Session: Access the database
    :return: A dictionary
    :doc-author: Trelent
    """
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()  # SELECT 1 - це все добре
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
