"""
Data models for breeders, litters, and AKC awards.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class AKCAwardType(Enum):
    """Types of AKC awards and titles."""
    # Conformation Titles
    CHAMPION = "CH"  # AKC Champion
    GRAND_CHAMPION = "GCH"  # Grand Champion
    GRAND_CHAMPION_BRONZE = "GCHB"
    GRAND_CHAMPION_SILVER = "GCHS"
    GRAND_CHAMPION_GOLD = "GCHG"
    GRAND_CHAMPION_PLATINUM = "GCHP"

    # Performance Titles
    COMPANION_DOG = "CD"
    COMPANION_DOG_EXCELLENT = "CDX"
    UTILITY_DOG = "UD"
    RALLY_NOVICE = "RN"
    RALLY_ADVANCED = "RA"
    RALLY_EXCELLENT = "RE"
    RALLY_MASTER = "RM"

    # Lure Coursing
    JUNIOR_COURSER = "JC"
    SENIOR_COURSER = "SC"
    MASTER_COURSER = "MC"
    FIELD_CHAMPION = "FC"
    LURE_COURSER_EXCELLENT = "LCX"

    # Agility
    NOVICE_AGILITY = "NA"
    OPEN_AGILITY = "OA"
    AGILITY_EXCELLENT = "AX"
    MASTER_AGILITY_CHAMPION = "MACH"

    # Canine Good Citizen
    CGC = "CGC"
    CGCA = "CGCA"  # Advanced
    CGCU = "CGCU"  # Urban

    # Health Certifications (CHIC)
    CHIC = "CHIC"  # Canine Health Information Center

    # Breeder Awards
    BREEDER_OF_MERIT = "BOM"
    BREEDER_OF_MERIT_GOLD = "BOM_GOLD"
    BRED_WITH_HEART = "BWH"


@dataclass
class AKCAward:
    """Represents an AKC award or title."""
    award_type: AKCAwardType
    dog_name: str
    date_earned: Optional[datetime] = None
    registration_number: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Human-readable award name."""
        names = {
            AKCAwardType.CHAMPION: "AKC Champion",
            AKCAwardType.GRAND_CHAMPION: "Grand Champion",
            AKCAwardType.GRAND_CHAMPION_BRONZE: "Grand Champion Bronze",
            AKCAwardType.GRAND_CHAMPION_SILVER: "Grand Champion Silver",
            AKCAwardType.GRAND_CHAMPION_GOLD: "Grand Champion Gold",
            AKCAwardType.GRAND_CHAMPION_PLATINUM: "Grand Champion Platinum",
            AKCAwardType.FIELD_CHAMPION: "Field Champion",
            AKCAwardType.MASTER_AGILITY_CHAMPION: "Master Agility Champion",
            AKCAwardType.BREEDER_OF_MERIT: "AKC Breeder of Merit",
            AKCAwardType.BREEDER_OF_MERIT_GOLD: "AKC Breeder of Merit Gold",
            AKCAwardType.BRED_WITH_HEART: "Bred with H.E.A.R.T.",
            AKCAwardType.CHIC: "CHIC Health Certified",
        }
        return names.get(self.award_type, self.award_type.value)

    def to_dict(self) -> dict:
        return {
            "award_type": self.award_type.value,
            "dog_name": self.dog_name,
            "date_earned": self.date_earned.isoformat() if self.date_earned else None,
            "registration_number": self.registration_number,
            "display_name": self.display_name
        }


@dataclass
class HealthTest:
    """Health testing record for breeding dogs."""
    test_type: str  # e.g., "Hip", "Elbow", "Thyroid", "Cardiac", "DM", "EOAD"
    result: str  # e.g., "OFA Good", "OFA Excellent", "Clear", "Normal"
    dog_name: str
    date_tested: Optional[datetime] = None
    certificate_number: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "test_type": self.test_type,
            "result": self.result,
            "dog_name": self.dog_name,
            "date_tested": self.date_tested.isoformat() if self.date_tested else None,
            "certificate_number": self.certificate_number
        }


@dataclass
class LitterImage:
    """Image of a litter or puppy."""
    image_path: str  # Local path or URL
    caption: Optional[str] = None
    date_taken: Optional[datetime] = None
    puppy_age_weeks: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "image_path": self.image_path,
            "caption": self.caption,
            "date_taken": self.date_taken.isoformat() if self.date_taken else None,
            "puppy_age_weeks": self.puppy_age_weeks
        }


@dataclass
class Litter:
    """Represents a litter of puppies."""
    litter_id: str
    sire_name: str
    dam_name: str
    birth_date: datetime
    num_puppies: int
    images: list[LitterImage] = field(default_factory=list)
    available_puppies: int = 0
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "litter_id": self.litter_id,
            "sire_name": self.sire_name,
            "dam_name": self.dam_name,
            "birth_date": self.birth_date.isoformat(),
            "num_puppies": self.num_puppies,
            "images": [img.to_dict() for img in self.images],
            "available_puppies": self.available_puppies,
            "description": self.description
        }


@dataclass
class Breeder:
    """Represents a Rhodesian Ridgeback breeder."""
    breeder_id: str
    kennel_name: str
    owner_name: str
    location: str  # City, State
    state: str
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    akc_awards: list[AKCAward] = field(default_factory=list)
    health_tests: list[HealthTest] = field(default_factory=list)
    litters: list[Litter] = field(default_factory=list)
    years_breeding: int = 0
    rrcus_member: bool = False  # Rhodesian Ridgeback Club of the US
    description: Optional[str] = None

    @property
    def total_champions(self) -> int:
        """Count of champion titles earned."""
        champion_types = {
            AKCAwardType.CHAMPION,
            AKCAwardType.GRAND_CHAMPION,
            AKCAwardType.GRAND_CHAMPION_BRONZE,
            AKCAwardType.GRAND_CHAMPION_SILVER,
            AKCAwardType.GRAND_CHAMPION_GOLD,
            AKCAwardType.GRAND_CHAMPION_PLATINUM,
            AKCAwardType.FIELD_CHAMPION,
        }
        return sum(1 for award in self.akc_awards if award.award_type in champion_types)

    @property
    def has_breeder_of_merit(self) -> bool:
        """Check if breeder has AKC Breeder of Merit status."""
        bom_types = {AKCAwardType.BREEDER_OF_MERIT, AKCAwardType.BREEDER_OF_MERIT_GOLD}
        return any(award.award_type in bom_types for award in self.akc_awards)

    @property
    def has_chic_dogs(self) -> bool:
        """Check if breeder has CHIC-certified dogs."""
        return any(award.award_type == AKCAwardType.CHIC for award in self.akc_awards)

    @property
    def award_score(self) -> int:
        """Calculate a score based on awards for ranking."""
        score = 0
        award_points = {
            AKCAwardType.GRAND_CHAMPION_PLATINUM: 100,
            AKCAwardType.GRAND_CHAMPION_GOLD: 80,
            AKCAwardType.GRAND_CHAMPION_SILVER: 60,
            AKCAwardType.GRAND_CHAMPION_BRONZE: 50,
            AKCAwardType.GRAND_CHAMPION: 40,
            AKCAwardType.CHAMPION: 30,
            AKCAwardType.FIELD_CHAMPION: 50,
            AKCAwardType.MASTER_AGILITY_CHAMPION: 50,
            AKCAwardType.BREEDER_OF_MERIT_GOLD: 100,
            AKCAwardType.BREEDER_OF_MERIT: 75,
            AKCAwardType.BRED_WITH_HEART: 25,
            AKCAwardType.CHIC: 50,
            AKCAwardType.MASTER_COURSER: 30,
            AKCAwardType.SENIOR_COURSER: 20,
            AKCAwardType.JUNIOR_COURSER: 10,
        }
        for award in self.akc_awards:
            score += award_points.get(award.award_type, 5)

        # Bonus for health testing
        score += len(self.health_tests) * 10

        # Bonus for RRCUS membership
        if self.rrcus_member:
            score += 25

        return score

    @property
    def most_recent_litter(self) -> Optional[Litter]:
        """Get the most recent litter."""
        if not self.litters:
            return None
        return max(self.litters, key=lambda l: l.birth_date)

    @property
    def latest_litter_images(self) -> list[LitterImage]:
        """Get images from the most recent litter."""
        recent = self.most_recent_litter
        if not recent:
            return []
        return sorted(recent.images, key=lambda i: i.date_taken or datetime.min, reverse=True)

    def to_dict(self) -> dict:
        return {
            "breeder_id": self.breeder_id,
            "kennel_name": self.kennel_name,
            "owner_name": self.owner_name,
            "location": self.location,
            "state": self.state,
            "website": self.website,
            "email": self.email,
            "phone": self.phone,
            "akc_awards": [award.to_dict() for award in self.akc_awards],
            "health_tests": [test.to_dict() for test in self.health_tests],
            "litters": [litter.to_dict() for litter in self.litters],
            "years_breeding": self.years_breeding,
            "rrcus_member": self.rrcus_member,
            "description": self.description,
            "total_champions": self.total_champions,
            "has_breeder_of_merit": self.has_breeder_of_merit,
            "has_chic_dogs": self.has_chic_dogs,
            "award_score": self.award_score
        }
