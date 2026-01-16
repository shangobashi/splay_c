"""Scan schemas for request/response validation."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductMatchResponse(BaseModel):
    """Product match information."""
    product_id: int
    name: str
    brand: str
    price: float
    currency: str
    image_url: Optional[str] = None
    retailer_name: str
    retailer_url: Optional[str] = None
    affiliate_url: Optional[str] = None
    similarity_score: float
    rank: int
    is_budget_alternative: bool

    class Config:
        from_attributes = True


class DetectedItemResponse(BaseModel):
    """Detected furniture item with matches."""
    item_id: str
    category: str
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float
    confidence: float
    crop_url: Optional[str] = None
    matches: List[ProductMatchResponse] = []

    class Config:
        from_attributes = True


class ScanResponse(BaseModel):
    """Scan with detected items."""
    scan_id: str
    user_id: str
    image_url: str
    thumbnail_url: Optional[str] = None
    status: str
    item_count: int = 0
    detected_items: List[DetectedItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScanListItemResponse(BaseModel):
    """Scan list item (without full detected items)."""
    scan_id: str
    thumbnail_url: Optional[str] = None
    status: str
    item_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ScanListResponse(BaseModel):
    """Paginated list of scans."""
    scans: List[ScanListItemResponse]
    total: int
    skip: int
    limit: int
