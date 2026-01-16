"""
Litter image gallery module for viewing and managing breeder images.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from .models import Breeder, Litter, LitterImage


@dataclass
class GalleryImage:
    """Extended image info for gallery display."""
    image_path: str
    breeder_id: str
    kennel_name: str
    litter_id: str
    sire_name: str
    dam_name: str
    birth_date: datetime
    caption: Optional[str] = None
    date_taken: Optional[datetime] = None
    puppy_age_weeks: Optional[int] = None

    @property
    def display_title(self) -> str:
        """Generate display title for the image."""
        parts = [self.kennel_name]
        if self.puppy_age_weeks:
            parts.append(f"{self.puppy_age_weeks} weeks")
        return " - ".join(parts)

    @property
    def parent_info(self) -> str:
        """Get sire x dam info."""
        return f"{self.sire_name} x {self.dam_name}"

    def to_dict(self) -> dict:
        return {
            "image_path": self.image_path,
            "breeder_id": self.breeder_id,
            "kennel_name": self.kennel_name,
            "litter_id": self.litter_id,
            "sire_name": self.sire_name,
            "dam_name": self.dam_name,
            "birth_date": self.birth_date.isoformat(),
            "caption": self.caption,
            "date_taken": self.date_taken.isoformat() if self.date_taken else None,
            "puppy_age_weeks": self.puppy_age_weeks,
            "display_title": self.display_title,
            "parent_info": self.parent_info
        }


class LitterGallery:
    """Service for browsing litter images across all breeders."""

    def __init__(self, breeders: list[Breeder]):
        self.breeders = breeders

    def get_all_images(self) -> list[GalleryImage]:
        """Get all litter images from all breeders."""
        images = []
        for breeder in self.breeders:
            for litter in breeder.litters:
                for img in litter.images:
                    images.append(GalleryImage(
                        image_path=img.image_path,
                        breeder_id=breeder.breeder_id,
                        kennel_name=breeder.kennel_name,
                        litter_id=litter.litter_id,
                        sire_name=litter.sire_name,
                        dam_name=litter.dam_name,
                        birth_date=litter.birth_date,
                        caption=img.caption,
                        date_taken=img.date_taken,
                        puppy_age_weeks=img.puppy_age_weeks
                    ))
        return images

    def get_recent_images(self, limit: int = 20) -> list[GalleryImage]:
        """Get most recently added images."""
        images = self.get_all_images()
        # Sort by date taken (newest first), with None dates at the end
        images.sort(
            key=lambda i: i.date_taken or datetime.min,
            reverse=True
        )
        return images[:limit]

    def get_images_by_breeder(self, breeder_id: str) -> list[GalleryImage]:
        """Get all images for a specific breeder."""
        return [
            img for img in self.get_all_images()
            if img.breeder_id == breeder_id
        ]

    def get_images_by_litter(self, breeder_id: str, litter_id: str) -> list[GalleryImage]:
        """Get all images for a specific litter."""
        return [
            img for img in self.get_all_images()
            if img.breeder_id == breeder_id and img.litter_id == litter_id
        ]

    def get_recent_litters(self, limit: int = 10) -> list[dict]:
        """Get most recent litters with their images."""
        litters = []
        for breeder in self.breeders:
            for litter in breeder.litters:
                litters.append({
                    "breeder_id": breeder.breeder_id,
                    "kennel_name": breeder.kennel_name,
                    "litter": litter.to_dict(),
                    "birth_date": litter.birth_date,
                    "image_count": len(litter.images)
                })

        # Sort by birth date (newest first)
        litters.sort(key=lambda l: l["birth_date"], reverse=True)
        return litters[:limit]

    def get_breeder_latest_litter_images(self, breeder_id: str) -> list[GalleryImage]:
        """Get images from a breeder's most recent litter."""
        breeder = next(
            (b for b in self.breeders if b.breeder_id == breeder_id),
            None
        )
        if not breeder or not breeder.litters:
            return []

        latest = max(breeder.litters, key=lambda l: l.birth_date)
        return self.get_images_by_litter(breeder_id, latest.litter_id)


def get_image_url(image_path: str, base_url: str = "/static/images") -> str:
    """Convert image path to URL for web display."""
    if image_path.startswith(("http://", "https://")):
        return image_path
    # Assume local path relative to images directory
    return f"{base_url}/{image_path}"
