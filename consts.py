from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

SECRET_KEY = "change-me-in-production-please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_LINK = "db.sql"
# DB_LINK = "test.sql"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
templates = Jinja2Templates(directory="static")
email = ("@gmail.com", "@yandex.ru", "@mail.ru")
allowed_files = ("png", "jfif", "jpg", "jpeg", "webp", "svg", "tiff", "psd")
easy_passwords = (
    "123456",
    "1234567",
    "12345678",
    "123456789",
    "1234567890",
    "password",
    "UNKNOWN",
    "000000",
    "admin123"
)
bad_words = ("beech", "блядь", "asshole", "fuck", "fucker", "пидор", "педик", "хуй", "хуйлан", "пидорас", "пизда")