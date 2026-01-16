"""Scan management routes."""
import uuid
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from PIL import Image
import io

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.scan import Scan, DetectedItem, ItemMatch
from app.models.product import Product
from app.schemas.scan import ScanResponse, ScanListResponse, DetectedItemResponse
from app.services.storage import storage_service
from app.services.vision import vision_provider
from app.services.matching import generate_stub_embedding, find_matching_products, rank_products


router = APIRouter()


# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MIN_IMAGE_SIZE = (400, 400)
MAX_IMAGE_SIZE = (4000, 4000)


def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file.

    Args:
        file: Uploaded file

    Raises:
        HTTPException: If validation fails
    """
    # Check extension
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )


@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process room image.

    Args:
        file: Image file to scan
        current_user: Authenticated user
        db: Database session

    Returns:
        Scan with detected items and product matches

    Raises:
        HTTPException: If validation fails or processing error
    """
    # Validate image
    validate_image(file)

    # Read and validate image data
    try:
        image_data = await file.read()

        if len(image_data) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Open with PIL to validate
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size

        if width < MIN_IMAGE_SIZE[0] or height < MIN_IMAGE_SIZE[1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too small. Minimum size: {MIN_IMAGE_SIZE[0]}x{MIN_IMAGE_SIZE[1]}"
            )

        if width > MAX_IMAGE_SIZE[0] or height > MAX_IMAGE_SIZE[1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image too large. Maximum size: {MAX_IMAGE_SIZE[0]}x{MAX_IMAGE_SIZE[1]}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file: {str(e)}"
        )

    # Reset file pointer for storage
    await file.seek(0)

    try:
        # Save image
        image_url, thumbnail_url = storage_service.save_upload(file.file, file.filename)

        # Create scan record
        scan = Scan(
            scan_id=str(uuid.uuid4()),
            user_id=current_user.user_id,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
            status="processing"
        )
        db.add(scan)
        db.flush()  # Get scan.id

        # Process image synchronously (no worker in no-Docker setup)
        # Detect furniture
        image_path = storage_service.get_file_path(image_url)
        detections = vision_provider.detect_furniture(str(image_path))

        # Process each detected item
        for detection in detections:
            # Create crop
            crop_url = storage_service.save_crop(
                image_url,
                detection.bbox,
                f"{scan.scan_id}_{detection.category}"
            )

            # Generate embedding
            embedding_text = f"{detection.category} furniture"
            embedding_vector = generate_stub_embedding(embedding_text)

            # Find matching products
            matches = find_matching_products(
                detection.category,
                embedding_vector,
                db,
                limit=20
            )

            # Rank products
            ranked_products = rank_products(matches, top_n=6)

            # Create detected item
            detected_item = DetectedItem(
                item_id=str(uuid.uuid4()),
                scan_id=scan.scan_id,
                category=detection.category,
                bbox_x=detection.bbox[0],
                bbox_y=detection.bbox[1],
                bbox_width=detection.bbox[2],
                bbox_height=detection.bbox[3],
                confidence=detection.confidence,
                crop_url=crop_url,
                embedding={"vector": embedding_vector}
            )
            db.add(detected_item)
            db.flush()  # Get detected_item.id

            # Create item matches
            for product_data in ranked_products:
                item_match = ItemMatch(
                    match_id=str(uuid.uuid4()),
                    item_id=detected_item.item_id,
                    product_id=product_data["product_id"],
                    similarity_score=product_data["similarity_score"],
                    rank=product_data["rank"],
                    is_budget_alternative=product_data["is_budget_alternative"]
                )
                db.add(item_match)

        # Update scan status
        scan.status = "completed"
        scan.item_count = len(detections)

        db.commit()
        db.refresh(scan)

        # Load relationships for response
        scan_with_items = db.query(Scan).filter(Scan.scan_id == scan.scan_id).first()

        return scan_with_items

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing scan: {str(e)}"
        )


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get scan by ID.

    Args:
        scan_id: Scan identifier
        current_user: Authenticated user
        db: Database session

    Returns:
        Scan with detected items and matches

    Raises:
        HTTPException: If scan not found or unauthorized
    """
    scan = db.query(Scan).filter(Scan.scan_id == scan_id).first()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    # Check ownership
    if scan.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this scan"
        )

    return scan


@router.get("", response_model=ScanListResponse)
async def list_scans(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's scans.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Authenticated user
        db: Database session

    Returns:
        List of scans with pagination
    """
    # Get total count
    total = db.query(Scan).filter(Scan.user_id == current_user.user_id).count()

    # Get scans
    scans = (
        db.query(Scan)
        .filter(Scan.user_id == current_user.user_id)
        .order_by(Scan.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return ScanListResponse(
        scans=scans,
        total=total,
        skip=skip,
        limit=limit
    )


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete scan by ID.

    Args:
        scan_id: Scan identifier
        current_user: Authenticated user
        db: Database session

    Raises:
        HTTPException: If scan not found or unauthorized
    """
    scan = db.query(Scan).filter(Scan.scan_id == scan_id).first()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    # Check ownership
    if scan.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this scan"
        )

    # Delete scan (cascade will delete detected items and matches)
    db.delete(scan)
    db.commit()

    return None
