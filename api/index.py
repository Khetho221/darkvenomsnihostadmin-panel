from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from core.auth import verify_pw, require_admin
from core.db import SessionLocal
from core.models import User, PassKey, Admin
from datetime import datetime, timedelta
import secrets, hashlib

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="CHANGE_THIS_SECRET")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_pw(password, admin.password_hash):
        return RedirectResponse("/", status_code=302)
    request.session["admin"] = username
    return RedirectResponse("/users", status_code=302)

@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request):
    require_admin(request)
    db = SessionLocal()
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users
    })

@app.post("/users/{username}/passkey")
def generate_passkey(username: str, request: Request):
    require_admin(request)
    raw = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    db = SessionLocal()
    pk = PassKey(
        username=username,
        passkey_hash=hashed,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(pk)
    db.commit()
    return {"passkey": raw}

@app.post("/users/{username}/ban")
def ban_user(username: str, request: Request):
    require_admin(request)
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    user.status = "banned"
    db.commit()
    return RedirectResponse("/users", status_code=302)
