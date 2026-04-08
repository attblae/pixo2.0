from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

SECRET_KEY = "change-me-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_LINK = "db.sql"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
templates = Jinja2Templates(directory="static")