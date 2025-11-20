import pytest

from app.models.incident import IncidentSource, IncidentStatus

pytestmark = [pytest.mark.integration, pytest.mark.endpoints]


def test_create_incident(client):
    """Test creating a new incident."""
    payload = {
        "description": "Test incident description",
        "source": IncidentSource.operator,
        "status": IncidentStatus.new,
    }
    response = client.post("/api/v1/incidents/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["description"] == payload["description"]
    assert body["source"] == payload["source"]
    assert body["status"] == payload["status"]
    assert "id" in body
    assert "created_at" in body


def test_create_incident_with_default_status(client):
    """Test creating an incident without specifying status (should default to new)."""
    post_body = {
        "description": "Test incident with default status",
        "source": IncidentSource.monitoring,
    }
    response = client.post("/api/v1/incidents/", json=post_body)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == IncidentStatus.new


def test_list_incidents_empty(client):
    """Test listing incidents when none exist."""
    response = client.get("/api/v1/incidents/")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 0


def test_list_incidents(client, incidents):
    """Test listing incidents."""
    response = client.get("/api/v1/incidents/")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == len(incidents)
    assert body[0]["description"] == "Second incident"
    assert body[1]["description"] == "First incident"


def test_list_incidents_filtered_by_status(client, incidents):
    """Test listing incidents filtered by status."""
    response = client.get("/api/v1/incidents/?status=new")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["status"] == IncidentStatus.new
    assert body[0]["description"] == "First incident"


def test_get_incident_by_id(client, incident):
    """Ensure a single incident can be fetched."""
    response = client.get(f"/api/v1/incidents/{incident.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == incident.id
    assert body["description"] == incident.description
    assert body["status"] == incident.status


def test_update_incident_status(client, incident):
    """Test updating an incident's status."""
    update_payload = {"status": IncidentStatus.resolved}
    response = client.patch(f"/api/v1/incidents/{incident.id}/status", json=update_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == IncidentStatus.resolved
    assert body["id"] == incident.id


def test_update_nonexistent_incident_status(client):
    """Test updating status of a non-existent incident."""
    update_payload = {"status": IncidentStatus.resolved}
    response = client.patch("/api/v1/incidents/99999/status", json=update_payload)

    assert response.status_code == 404
    body = response.json()
    assert "not found" in body["detail"].lower()
