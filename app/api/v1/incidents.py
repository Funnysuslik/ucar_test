from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import SessionDep
from app.crud.incidents import create_incident as crud_create_incident
from app.crud.incidents import get_incident, get_incidents
from app.crud.incidents import update_incident_status as crud_update_incident_status
from app.models import (
    Incident,
    IncidentCreate,
    IncidentRead,
    IncidentStatus,
    IncidentUpdateStatus,
)

incidents_router = APIRouter(prefix="/incidents", tags=["incidents"])


@incidents_router.post("/", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, session: SessionDep) -> Incident:
    """Create a new incident."""
    return crud_create_incident(session=session, incident=payload)


@incidents_router.get("/", response_model=list[IncidentRead])
def list_incidents(
    session: SessionDep,
    status_filter: IncidentStatus | None = Query(default=None, alias="status"),
) -> list[Incident]:
    """List incidents, optionally filtered by status."""
    return get_incidents(session=session, status_filter=status_filter)


@incidents_router.get("/{incident_id}", response_model=IncidentRead)
def get_incident_by_id(incident_id: int, session: SessionDep) -> Incident:
    """Retrieve a single incident."""
    incident = get_incident(session=session, incident_id=incident_id)
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@incidents_router.patch("/{incident_id}/status", response_model=IncidentRead)
def update_incident_status(
    incident_id: int,
    payload: IncidentUpdateStatus,
    session: SessionDep,
) -> Incident:
    """Update an incident's status."""
    incident = get_incident(session=session, incident_id=incident_id)
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return crud_update_incident_status(session=session, incident=incident, status=payload.status)
