from datetime import datetime

from sqlalchemy import create_engine, URL, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

credentials = {
    'username': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'database': 'postgres',
    'port': 5433,
}

db_url = URL.create(
    'postgresql+psycopg2',
    username=credentials['username'],
    password=credentials['password'],
    host=credentials['host'],
    port=credentials['port'],
    database=credentials['database'])

engine = create_engine(db_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class BaseSqlModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)