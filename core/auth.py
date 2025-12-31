from passlib.hash import bcrypt
from fastapi import Request, HTTPException

def hash_pw(pw):
    return bcrypt.hash(pw)

def verify_pw(pw, hashed):
    return bcrypt.verify(pw, hashed)

def require_admin(request: Request):
    if not request.session.get("admin"):
        raise HTTPException(status_code=401)
