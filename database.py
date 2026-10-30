import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

# Некоторые хостинги (Render, Heroku) отдают postgres://, SQLAlchemy 2.0 такой префикс не принимает
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

is_sqlite = SQLALCHEMY_DATABASE_URL.startswith("sqlite")

# check_same_thread нужен только для SQLite
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

if is_sqlite:

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, _):
        # В SQLite внешние ключи по умолчанию выключены
        dbapi_connection.execute("PRAGMA foreign_keys=ON")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
