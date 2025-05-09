import pytest
import asyncio
import os
from httpx import AsyncClient

from app.main import app
from app.db.database import Base as app_Base, engine as app_engine, SessionLocal
from app.core.config import settings

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def initialize_db(): # Synchronous fixture
    """Initialize a clean database before running tests and drop it afterwards."""
    if not settings.DATABASE_URL:
        raise Exception("DATABASE_URL is not set. Please set it as an environment variable for tests, e.g., 'export DATABASE_URL=sqlite:///./test_ecommerce_pytest.db'")
    
    if app_engine is None:
        # This case should be prevented by the check above, as settings.DATABASE_URL being None would lead to engine being None in app.db.database
        raise Exception("Database engine in app.db.database is None. This typically means DATABASE_URL was not set when the app modules were imported.")

    # Using the synchronous engine from the app, configured by DATABASE_URL env var
    app_Base.metadata.drop_all(bind=app_engine) # Clean slate
    app_Base.metadata.create_all(bind=app_engine) # Create tables
    yield
    app_Base.metadata.drop_all(bind=app_engine) # Clean up
    
    # If using a file-based SQLite, delete the file after tests
    db_path = None
    if "sqlite" in str(app_engine.url.drivername):
        db_path = app_engine.url.database
    
    if db_path and db_path != ":memory:" and os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Test database file {db_path} removed.")
        except OSError as e:
            print(f"Error removing test database file {db_path}: {e}")

@pytest.fixture(scope="function")
def db_session() -> SessionLocal: # Synchronous fixture providing a session
    """Fixture para fornecer uma sessão de banco de dados para os testes."""
    session = SessionLocal() # SessionLocal is bound to the app_engine
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
async def client(initialize_db) -> AsyncClient:
    """An HTTP client, with a fresh database, for testing the API."""
    # initialize_db fixture ensures DB is set up
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture(scope="function")
async def admin_auth_headers(client: AsyncClient) -> dict:
    """Retorna headers de autenticação para o usuário admin."""
    # This relies on the startup event in main.py to create the admin user.
    # If DATABASE_URL was just set, the app startup event needs to run against the new test DB.
    # Pytest typically re-imports the app or handles this, but explicit re-init might be needed if issues persist.
    
    login_data = {
        "username": settings.ADMIN_EMAIL,
        "password": settings.ADMIN_PASSWORD
    }
    response = await client.post("/auth/login", data=login_data)
    
    if response.status_code != 200:
        # This might happen if the admin user wasn't created in the test DB by the startup event.
        # For robustness, one might consider programmatically ensuring admin exists here if login fails.
        print(f"Admin login failed during test setup: {response.status_code} - {response.text}")
        print(f"Attempted with ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
        # As a fallback, try to create the admin user if the app's startup event didn't cover it for the test session.
        # This requires db_session to be available or direct db interaction.
        # For now, we'll raise an exception if login fails, as tests depend on it.
        raise Exception(f"Falha ao logar como admin para obter token: {response.text}. Verifique se o usuário admin é criado no banco de dados de teste.")
            
    tokens = response.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

