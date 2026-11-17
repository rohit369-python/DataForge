"""Pipeline configuration, execution, and run-history endpoints."""
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models import DataSource, Pipeline, PipelineRun
from backend.app.schemas import PipelineCreate, PipelineUpdate
from backend.app.services import execute_demo
from backend.app.api.monitoring import run_dict

router = APIRouter(prefix="/api/v1", tags=["pipelines"])


def pipeline_dict(pipeline: Pipeline) -> dict:
    """Convert a pipeline ORM object into an API response."""
    return {
        "id": pipeline.id,
        "name": pipeline.name,
        "description": pipeline.description,
        "source_id": pipeline.source_id,
        "active": pipeline.active,
        "schedule": pipeline.schedule,
        "created_at": pipeline.created_at.isoformat() if pipeline.created_at else None,
    }


@router.post("/pipelines", status_code=201)
def create_pipeline(payload: PipelineCreate, db: Session = Depends(get_db)):
    """Create a pipeline after validating its name and optional source."""
    existing = db.scalar(select(Pipeline).where(Pipeline.name == payload.name))
    if existing:
        raise HTTPException(409, "Pipeline name already exists")
    if payload.source_id and not db.get(DataSource, payload.source_id):
        raise HTTPException(404, "Source not found")
    pipeline = Pipeline(**payload.model_dump())
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline_dict(pipeline)


@router.get("/pipelines")
def list_pipelines(db: Session = Depends(get_db)):
    """List configured pipelines, newest first."""
    pipelines = db.scalars(select(Pipeline).order_by(Pipeline.id.desc())).all()
    return [pipeline_dict(pipeline) for pipeline in pipelines]


@router.patch("/pipelines/{pipeline_id}")
def update_pipeline(pipeline_id: int, payload: PipelineUpdate, db: Session = Depends(get_db)):
    """Update only the fields explicitly supplied by the caller."""
    pipeline = db.get(Pipeline, pipeline_id)
    if not pipeline:
        raise HTTPException(404, "Pipeline not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pipeline, field, value)
    db.commit()
    db.refresh(pipeline)
    return pipeline_dict(pipeline)


@router.post("/pipelines/{pipeline_id}/run")
def run_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    """Execute the project's demo batch and persist its run result."""
    pipeline = db.get(Pipeline, pipeline_id)
    if not pipeline:
        raise HTTPException(404, "Pipeline not found")
    if not pipeline.active:
        raise HTTPException(409, "Pipeline is paused")

    run = PipelineRun(pipeline_id=pipeline.id, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    start = time.perf_counter()
    try:
        result = execute_demo()
        run.status = "success"
        run.records_extracted = result["records_extracted"]
        run.records_processed = result["records_processed"]
        run.records_rejected = result["records_rejected"]
        run.message = "Demo batch completed; Bronze, Silver and Gold artifacts written."
    except Exception as exc:
        run.status = "failed"
        run.message = f"Execution failed: {type(exc).__name__}"
    run.duration_seconds = round(time.perf_counter() - start, 3)
    db.commit()
    db.refresh(run)
    return run_dict(run)


@router.get("/runs")
def list_runs(db: Session = Depends(get_db)):
    """Return the latest 100 pipeline runs."""
    runs = db.scalars(select(PipelineRun).order_by(PipelineRun.id.desc()).limit(100)).all()
    return [run_dict(run) for run in runs]
