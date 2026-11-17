"""Data-source management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models import DataSource
from backend.app.schemas import SourceCreate

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


def source_dict(source: DataSource) -> dict:
    """Convert a data-source ORM object into an API response."""
    return {
        "id": source.id,
        "name": source.name,
        "source_type": source.source_type,
        "description": source.description,
        "status": source.status,
        "created_at": source.created_at.isoformat() if source.created_at else None,
    }


@router.post("", status_code=201)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    """Register a data source, rejecting duplicate names."""
    existing = db.scalar(select(DataSource).where(DataSource.name == payload.name))
    if existing:
        raise HTTPException(409, "Source name already exists")
    source = DataSource(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source_dict(source)


@router.get("")
def list_sources(db: Session = Depends(get_db)):
    """List registered data sources, newest first."""
    sources = db.scalars(select(DataSource).order_by(DataSource.id.desc())).all()
    return [source_dict(source) for source in sources]


@router.delete("/{source_id}", status_code=204)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Delete a data source by its database identifier."""
    source = db.get(DataSource, source_id)
    if not source:
        raise HTTPException(404, "Source not found")
    db.delete(source)
    db.commit()
