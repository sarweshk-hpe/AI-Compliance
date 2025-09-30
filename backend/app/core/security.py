from datetime import datetime, timedelta
from typing import Optional
import hashlib
import hmac
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.PyJWTError:
        return None

def create_hmac_signature(data: str) -> str:
    """Create HMAC signature for audit trail integrity"""
    signature = hmac.new(
        settings.hmac_secret_key.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"hmac-sha256:{signature}"

def verify_hmac_signature(data: str, signature: str) -> bool:
    """Verify HMAC signature"""
    expected_signature = create_hmac_signature(data)
    return hmac.compare_digest(signature, expected_signature)

def hash_input(input_data: str) -> str:
    """Create SHA256 hash of input data"""
    return hashlib.sha256(input_data.encode('utf-8')).hexdigest()
