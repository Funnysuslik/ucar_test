import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.core.database import get_session
from app.main import app
from app.models.incident import Incident, IncidentSource, IncidentStatus


@pytest.fixture(scope="function")
def engine():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})

    SQLModel.metadata.create_all(engine)

    yield engine
    engine.dispose()
    os.remove(path)


@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(engine):
    def _get_test_db():
        with Session(engine) as session:
            yield session

    from app.api.deps import get_db

    app.dependency_overrides[get_db] = _get_test_db

    test_client = TestClient(
        app,
        base_url="http://testserver",
        raise_server_exceptions=True,
    )
    with test_client as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def incident(session) -> Incident:
    """Persisted incident for read/update tests."""
    obj = Incident(
        description="Persisted incident",
        source=IncidentSource.operator,
        status=IncidentStatus.investigating,
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@pytest.fixture
def incidents(session) -> list[Incident]:
    """Multiple incidents stored in the database."""
    first = Incident(
        description="First incident",
        source=IncidentSource.operator,
        status=IncidentStatus.new,
    )
    second = Incident(
        description="Second incident",
        source=IncidentSource.monitoring,
        status=IncidentStatus.investigating,
    )
    session.add_all([first, second])
    session.commit()
    session.refresh(first)
    session.refresh(second)
    return [first, second]
