from sqlalchemy import create_engine
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from urllib.parse import quote_plus

# URL-encode username/password to safely include special characters
_DB_USER = quote_plus(DB_USER)
_DB_PASS = quote_plus(DB_PASS)

DATABASE_URL = (
    f"mysql+pymysql://{_DB_USER}:{_DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
