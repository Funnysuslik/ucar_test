from sqlmodel import Session, select

from app.models import Incident, IncidentCreate, IncidentStatus


def create_incident(*, session: Session, incident: IncidentCreate) -> Incident:
    """Create a new incident."""
    db_incident = Incident(**incident.model_dump())
    session.add(db_incident)
    session.commit()
    session.refresh(db_incident)
    return db_incident


def get_incidents(
    *, session: Session, status_filter: IncidentStatus | None = None, skip: int = 0, limit: int = 100
) -> list[Incident]:
    """Get incidents, optionally filtered by status."""
    statement = select(Incident).order_by(Incident.created_at.desc()).offset(skip).limit(limit)
    if status_filter is not None:
        statement = statement.where(Incident.status == status_filter)
    incidents = session.exec(statement).all()
    return incidents


def get_incident(*, session: Session, incident_id: int) -> Incident | None:
    """Get an incident by ID."""
    return session.get(Incident, incident_id)


def update_incident_status(*, session: Session, incident: Incident, status: IncidentStatus) -> Incident:
    """Update an incident's status."""
    incident.status = status
    session.add(incident)
    session.commit()
    session.refresh(incident)
    return incident
