"""Scan-related models."""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scan(Base):
    """Scan model representing a room photo analysis job."""

    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False, index=True
    )
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    share_token: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="scans")  # type: ignore # noqa: F821
    items: Mapped[List["DetectedItem"]] = relationship(
        "DetectedItem", back_populates="scan", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of Scan."""
        return f"<Scan(id={self.id}, status={self.status})>"


class DetectedItem(Base):
    """Detected furniture item in a scanned room."""

    __tablename__ = "detected_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    scan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("scans.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    bbox_x: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_y: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_width: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_height: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    crop_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Store as JSON for SQLite
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    scan: Mapped["Scan"] = relationship("Scan", back_populates="items")
    matches: Mapped[List["ItemMatch"]] = relationship(
        "ItemMatch", back_populates="item", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of DetectedItem."""
        return f"<DetectedItem(id={self.id}, category={self.category}, confidence={self.confidence:.2f})>"


class ItemMatch(Base):
    """Match between a detected item and a product."""

    __tablename__ = "item_matches"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("detected_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    is_budget_alternative: Mapped[bool] = mapped_column(Integer, default=0)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    item: Mapped["DetectedItem"] = relationship("DetectedItem", back_populates="matches")
    product: Mapped["Product"] = relationship("Product", back_populates="item_matches")  # type: ignore # noqa: F821

    def __repr__(self) -> str:
        """String representation of ItemMatch."""
        return f"<ItemMatch(item={self.item_id}, product={self.product_id}, score={self.similarity_score:.2f})>"
