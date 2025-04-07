import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import g

# Get database URL from environment variables or use SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Create SQLAlchemy engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# Create base class for models
Base = declarative_base()
Base.query = db_session.query_property()

# Function to get database session
def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

# Function to close database session
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Function to initialize database
def init_db():
    # Import all modules here that might define models
    import models
    Base.metadata.create_all(bind=engine)

# Function to teardown database session
def teardown_db(app):
    @app.teardown_appcontext
    def teardown(exception=None):
        close_db()
