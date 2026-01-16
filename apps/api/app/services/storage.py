"""Storage service for file uploads."""
import uuid
import shutil
from pathlib import Path
from typing import BinaryIO

from PIL import Image

from app.settings import settings


class StorageService:
    """Local file storage service."""

    def __init__(self):
        """Initialize storage service."""
        self.storage_path = settings.storage_dir
        self.uploads_path = self.storage_path / "uploads"
        self.thumbnails_path = self.storage_path / "thumbnails"
        self.crops_path = self.storage_path / "crops"

        # Create directories if they don't exist
        self.uploads_path.mkdir(parents=True, exist_ok=True)
        self.thumbnails_path.mkdir(parents=True, exist_ok=True)
        self.crops_path.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file: BinaryIO, filename: str) -> tuple[str, str]:
        """Save uploaded image and create thumbnail.

        Args:
            file: File object to save
            filename: Original filename

        Returns:
            Tuple of (image_url, thumbnail_url)
        """
        # Generate unique filename
        file_id = str(uuid.uuid4())
        ext = Path(filename).suffix or ".jpg"
        new_filename = f"{file_id}{ext}"

        # Save original image
        image_path = self.uploads_path / new_filename
        with open(image_path, "wb") as f:
            shutil.copyfileobj(file, f)

        # Create thumbnail
        thumbnail_path = self.thumbnails_path / new_filename
        self._create_thumbnail(image_path, thumbnail_path)

        # Return relative URLs
        image_url = f"/storage/uploads/{new_filename}"
        thumbnail_url = f"/storage/thumbnails/{new_filename}"

        return image_url, thumbnail_url

    def _create_thumbnail(self, image_path: Path, thumbnail_path: Path, size: tuple = (400, 400)):
        """Create thumbnail from image.

        Args:
            image_path: Path to original image
            thumbnail_path: Path to save thumbnail
            size: Thumbnail size (width, height)
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Create thumbnail maintaining aspect ratio
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(thumbnail_path, "JPEG", quality=85)
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            # Copy original as fallback
            shutil.copy(image_path, thumbnail_path)

    def save_crop(self, image_path: str, bbox: tuple, item_id: str) -> str:
        """Crop and save detected item from image.

        Args:
            image_path: Path to original image
            bbox: Bounding box (x, y, width, height) normalized 0-1
            item_id: Unique item identifier

        Returns:
            URL to cropped image
        """
        try:
            # Convert relative path to absolute
            if image_path.startswith("/storage/uploads/"):
                filename = image_path.split("/")[-1]
                full_path = self.uploads_path / filename
            else:
                full_path = Path(image_path)

            with Image.open(full_path) as img:
                # Convert normalized bbox to pixel coordinates
                x, y, w, h = bbox
                width, height = img.size

                left = int(x * width)
                top = int(y * height)
                right = int((x + w) * width)
                bottom = int((y + h) * height)

                # Crop image
                cropped = img.crop((left, top, right, bottom))

                # Save crop
                crop_filename = f"{item_id}.jpg"
                crop_path = self.crops_path / crop_filename

                if cropped.mode in ("RGBA", "P"):
                    cropped = cropped.convert("RGB")

                cropped.save(crop_path, "JPEG", quality=90)

                return f"/storage/crops/{crop_filename}"
        except Exception as e:
            print(f"Error creating crop: {e}")
            return ""

    def get_file_path(self, url: str) -> Path:
        """Convert storage URL to filesystem path.

        Args:
            url: Storage URL (e.g., /storage/uploads/abc.jpg)

        Returns:
            Absolute filesystem path
        """
        if url.startswith("/storage/"):
            relative_path = url.replace("/storage/", "")
            return self.storage_path / relative_path
        return Path(url)


# Global storage instance
storage_service = StorageService()
