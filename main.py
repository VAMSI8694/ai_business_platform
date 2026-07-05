from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid

from backend.database import get_db, engine
from backend.auth import (
    verify_password, get_password_hash, 
    create_access_token, verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from backend.schemas import (
    UserCreate, Token, AgentRequest, AgentResponse
)
from agents.orchestrator import orchestrator

app = FastAPI(
    title="AI Business Platform",
    description="Multi-Agent AI Business Management System",
    version="1.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Auth Routes ───────────────────────────────────────────────────
@app.post("/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    from sqlalchemy import text
    
    # Check if user exists
    result = db.execute(
        text("SELECT id FROM users WHERE username = :username OR email = :email"),
        {"username": user.username, "email": user.email}
    ).fetchone()
    
    if result:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    
    db.execute(
        text("INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :password)"),
        {"username": user.username, "email": user.email, "password": hashed_password}
    )
    db.commit()
    
    return {"message": "User created successfully", "username": user.username}

@app.post("/auth/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    from sqlalchemy import text
    
    user = db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": form_data.username}
    ).fetchone()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# ─── Agent Routes ───────────────────────────────────────────────────
@app.post("/agents/chat", response_model=AgentResponse)
async def chat_with_agent(
    request: AgentRequest,
    current_user: str = Depends(verify_token)
):
    session_id = request.session_id or str(uuid.uuid4())
    
    result = orchestrator.process_request(
        user_message=request.message,
        agent_override=request.agent_name if request.agent_name != "auto" else None,
        context=request.context
    )
    
    return AgentResponse(
        response=result["response"],
        agent_name=result.get("routed_to", request.agent_name),
        session_id=session_id,
        tokens_used=result.get("tokens_used", 0),
        success=result.get("success", True)
    )

@app.post("/agents/broadcast")
async def broadcast_to_all(
    request: AgentRequest,
    current_user: str = Depends(verify_token)
):
    result = orchestrator.broadcast_to_all_agents(
        message=request.message,
        context=request.context
    )
    return result

@app.get("/agents/list")
async def list_agents(current_user: str = Depends(verify_token)):
    return {
        "agents": [
            {"name": "accounts", "description": "Finance & Accounting"},
            {"name": "manufacturing", "description": "Manufacturing & Operations"},
            {"name": "purchase", "description": "Procurement & Purchasing"},
            {"name": "sales", "description": "Sales & Revenue"},
            {"name": "investment", "description": "Investment & Planning"},
        ]
    }

@app.post("/agents/reset")
async def reset_agents(current_user: str = Depends(verify_token)):
    orchestrator.reset_all_agents()
    return {"message": "All agent conversations reset"}

# ─── Health Check ───────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "healthy", "platform": "AI Business Platform v1.0"}

@app.get("/")
async def root():
    return {"message": "AI Business Platform API is running"}
