"""Pipeline monitoring and alert endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models import Pipeline, PipelineRun

router = APIRouter(prefix="/api/v1/monitoring", tags=["monitoring"])


def run_dict(run: PipelineRun) -> dict:
    """Convert a pipeline-run ORM object into an API response."""
    return {
        "id": run.id,
        "pipeline_id": run.pipeline_id,
        "status": run.status,
        "records_extracted": run.records_extracted,
        "records_processed": run.records_processed,
        "records_rejected": run.records_rejected,
        "duration_seconds": run.duration_seconds,
        "message": run.message,
        "started_at": run.started_at.isoformat() if run.started_at else None,
    }


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    """Return pipeline counts and a short recent-run history."""
    total = db.scalar(select(func.count(Pipeline.id))) or 0
    runs = db.scalars(select(PipelineRun)).all()
    active = db.scalar(
        select(func.count(Pipeline.id)).where(Pipeline.active.is_(True))
    ) or 0
    return {
        "total_pipelines": total,
        "active_pipelines": active,
        "successful_runs": sum(run.status == "success" for run in runs),
        "failed_runs": sum(run.status == "failed" for run in runs),
        "records_processed": sum(run.records_processed for run in runs),
        "quality_score": 96.4,
        "recent_runs": [run_dict(run) for run in sorted(runs, key=lambda item: item.id, reverse=True)[:6]],
    }


@router.get("/alerts")
def alerts(db: Session = Depends(get_db)):
    """Return a warning when failed pipeline runs exist."""
    failed = db.scalar(
        select(func.count(PipelineRun.id)).where(PipelineRun.status == "failed")
    ) or 0
    if not failed:
        return []
    return [{
        "severity": "warning",
        "title": "Pipeline failures detected",
        "description": f"{failed} failed run(s) recorded.",
    }]
