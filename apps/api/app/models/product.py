"""Product model."""
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, String, Text, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    """Product model representing furniture available for purchase."""

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    external_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    dimensions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    colors: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Store list as JSON
    materials: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Store list as JSON
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    images: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Store list as JSON
    affiliate_url: Mapped[str] = mapped_column(Text, nullable=False)
    retailer_url: Mapped[str] = mapped_column(Text, nullable=False)
    retailer_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    embedding: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Store vector as JSON
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_updated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    item_matches: Mapped[List["ItemMatch"]] = relationship(  # type: ignore # noqa: F821
        "ItemMatch", back_populates="product"
    )

    def __repr__(self) -> str:
        """String representation of Product."""
        return f"<Product(id={self.id}, name={self.name}, price=${self.price:.2f})>"
