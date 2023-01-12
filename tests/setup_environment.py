import os
import sys

sys.path.append(f'{os.getcwd()}/src')
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from main import app
from security import UserSession, get_current_user
from services.app_user_service import app_user_service
from setting import settings

db_connection_url = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(db_connection_url)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database once
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested transaction. Need to start a new one when that happens.
    @event.listens_for(session, 'after_transaction_end')
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()
    
# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        user = app_user_service.get_by_email(session, 'admin@ucars.sg')
        yield UserSession(user, session)

    app.dependency_overrides[get_current_user] = override_get_db
    yield TestClient(app)
    # del app.dependency_overrides[get_current_user]
