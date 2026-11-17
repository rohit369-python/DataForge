from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.core.database import Base
def now(): return datetime.now(timezone.utc)
class DataSource(Base):
    __tablename__ = "data_sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    source_type: Mapped[str] = mapped_column(String(40), default="csv")
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="configured")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
class Pipeline(Base):
    __tablename__ = "pipelines"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(140), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    schedule: Mapped[str] = mapped_column(String(80), default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    pipeline_id: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(20), default="running")
    records_extracted: Mapped[int] = mapped_column(Integer, default=0)
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    records_rejected: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0)
    message: Mapped[str] = mapped_column(Text, default="")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
