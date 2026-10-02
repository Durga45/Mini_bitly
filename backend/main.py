import os
import string
import random
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Environment se DATABASE_URL uthana (Docker compose / .env se)
# Agar nahi mila toh local testing ke liye SQLite use karega
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Table Model (SQLAlchemy)
class URLDB(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)

# Tables automatically create karne ke liye
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-Bitly API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URLRequest(BaseModel):
    original_url: str

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

@app.post("/shorten")
def shorten_url(payload: URLRequest, db: Session = Depends(get_db)):
    # Unique short code generate karna
    short_code = generate_short_code()
    while db.query(URLDB).filter(URLDB.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = URLDB(original_url=payload.original_url, short_code=short_code, clicks=0)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return {"short_code": short_code, "original_url": payload.original_url}

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URLDB).filter(URLDB.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
        
    # Click count increment karna (Analytics)
    db_url.clicks += 1
    db.commit()
    
    return RedirectResponse(url=db_url.original_url)

@app.get("/analytics/{short_code}")
def get_analytics(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URLDB).filter(URLDB.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
        
    return {"original_url": db_url.original_url, "short_code": short_code, "clicks": db_url.clicks}