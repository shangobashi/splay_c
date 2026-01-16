"""Vision service for furniture detection."""
from typing import List, Dict
from dataclasses import dataclass
import hashlib


@dataclass
class Detection:
    """Detected furniture item."""
    category: str
    bbox: tuple  # (x, y, width, height) normalized 0-1
    confidence: float


class StubVisionProvider:
    """Stub vision provider for MVP - returns deterministic detections."""

    def __init__(self):
        """Initialize stub provider."""
        self.categories = [
            "sofa", "coffee_table", "floor_lamp", "table_lamp",
            "dining_table", "chair", "side_table", "pendant_light"
        ]

    def detect_furniture(self, image_path: str) -> List[Detection]:
        """Detect furniture in image (stubbed with deterministic results).

        Args:
            image_path: Path to image file

        Returns:
            List of detected furniture items

        Note:
            This is a stub implementation. In production, this would call
            OpenAI Vision API or a custom-trained model.
        """
        # Generate deterministic detections based on image path
        # This ensures consistent results for testing
        image_hash = hashlib.md5(image_path.encode()).hexdigest()
        seed = int(image_hash[:8], 16)

        detections = []

        # Always detect a sofa (main furniture)
        detections.append(Detection(
            category="sofa",
            bbox=(0.15, 0.35, 0.50, 0.40),
            confidence=0.95
        ))

        # Always detect a coffee table
        detections.append(Detection(
            category="coffee_table",
            bbox=(0.35, 0.65, 0.30, 0.20),
            confidence=0.88
        ))

        # Conditionally detect lamp based on seed
        if seed % 2 == 0:
            detections.append(Detection(
                category="floor_lamp",
                bbox=(0.75, 0.15, 0.12, 0.50),
                confidence=0.82
            ))
        else:
            detections.append(Detection(
                category="table_lamp",
                bbox=(0.20, 0.25, 0.10, 0.15),
                confidence=0.79
            ))

        return detections

    def get_supported_categories(self) -> List[str]:
        """Get list of supported furniture categories.

        Returns:
            List of category names
        """
        return self.categories


class OpenAIVisionProvider:
    """OpenAI Vision provider (not implemented - requires API key)."""

    def __init__(self, api_key: str):
        """Initialize OpenAI provider."""
        self.api_key = api_key
        raise NotImplementedError(
            "OpenAI Vision provider not implemented. "
            "Use StubVisionProvider for MVP."
        )


# Global vision provider instance
vision_provider = StubVisionProvider()
