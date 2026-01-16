"""
Breeder finder service for searching and ranking breeders.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from .models import (
    Breeder, Litter, LitterImage, AKCAward, HealthTest,
    AKCAwardType
)


class BreederFinder:
    """Service for finding and ranking Rhodesian Ridgeback breeders."""

    def __init__(self, data_path: Optional[Path] = None):
        self.breeders: list[Breeder] = []
        self.data_path = data_path or Path(__file__).parent.parent / "data" / "breeders.json"

    def load_breeders(self) -> None:
        """Load breeders from JSON data file."""
        if not self.data_path.exists():
            return

        with open(self.data_path, 'r') as f:
            data = json.load(f)

        self.breeders = []
        for b in data.get("breeders", []):
            breeder = self._parse_breeder(b)
            self.breeders.append(breeder)

    def _parse_breeder(self, data: dict) -> Breeder:
        """Parse a breeder from dictionary data."""
        awards = []
        for a in data.get("akc_awards", []):
            try:
                award_type = AKCAwardType(a["award_type"])
            except ValueError:
                continue
            awards.append(AKCAward(
                award_type=award_type,
                dog_name=a.get("dog_name", ""),
                date_earned=datetime.fromisoformat(a["date_earned"]) if a.get("date_earned") else None,
                registration_number=a.get("registration_number")
            ))

        health_tests = []
        for h in data.get("health_tests", []):
            health_tests.append(HealthTest(
                test_type=h["test_type"],
                result=h["result"],
                dog_name=h.get("dog_name", ""),
                date_tested=datetime.fromisoformat(h["date_tested"]) if h.get("date_tested") else None,
                certificate_number=h.get("certificate_number")
            ))

        litters = []
        for l in data.get("litters", []):
            images = []
            for img in l.get("images", []):
                images.append(LitterImage(
                    image_path=img["image_path"],
                    caption=img.get("caption"),
                    date_taken=datetime.fromisoformat(img["date_taken"]) if img.get("date_taken") else None,
                    puppy_age_weeks=img.get("puppy_age_weeks")
                ))
            litters.append(Litter(
                litter_id=l["litter_id"],
                sire_name=l["sire_name"],
                dam_name=l["dam_name"],
                birth_date=datetime.fromisoformat(l["birth_date"]),
                num_puppies=l["num_puppies"],
                images=images,
                available_puppies=l.get("available_puppies", 0),
                description=l.get("description")
            ))

        return Breeder(
            breeder_id=data["breeder_id"],
            kennel_name=data["kennel_name"],
            owner_name=data["owner_name"],
            location=data["location"],
            state=data["state"],
            website=data.get("website"),
            email=data.get("email"),
            phone=data.get("phone"),
            akc_awards=awards,
            health_tests=health_tests,
            litters=litters,
            years_breeding=data.get("years_breeding", 0),
            rrcus_member=data.get("rrcus_member", False),
            description=data.get("description")
        )

    def save_breeders(self) -> None:
        """Save breeders to JSON data file."""
        data = {"breeders": [b.to_dict() for b in self.breeders]}
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def add_breeder(self, breeder: Breeder) -> None:
        """Add a new breeder to the database."""
        self.breeders.append(breeder)

    def get_breeder(self, breeder_id: str) -> Optional[Breeder]:
        """Get a specific breeder by ID."""
        for breeder in self.breeders:
            if breeder.breeder_id == breeder_id:
                return breeder
        return None

    def search(
        self,
        state: Optional[str] = None,
        min_champions: int = 0,
        require_breeder_of_merit: bool = False,
        require_chic: bool = False,
        require_rrcus: bool = False,
        has_available_puppies: bool = False,
        sort_by: str = "award_score"
    ) -> list[Breeder]:
        """
        Search for breeders with filters.

        Args:
            state: Filter by state (e.g., "CA", "TX")
            min_champions: Minimum number of champion titles
            require_breeder_of_merit: Only show AKC Breeder of Merit
            require_chic: Only show breeders with CHIC-certified dogs
            require_rrcus: Only show RRCUS members
            has_available_puppies: Only show breeders with available puppies
            sort_by: Sort field ("award_score", "champions", "name")

        Returns:
            List of matching breeders, sorted by the specified field
        """
        results = self.breeders.copy()

        # Apply filters
        if state:
            results = [b for b in results if b.state.upper() == state.upper()]

        if min_champions > 0:
            results = [b for b in results if b.total_champions >= min_champions]

        if require_breeder_of_merit:
            results = [b for b in results if b.has_breeder_of_merit]

        if require_chic:
            results = [b for b in results if b.has_chic_dogs]

        if require_rrcus:
            results = [b for b in results if b.rrcus_member]

        if has_available_puppies:
            results = [
                b for b in results
                if any(l.available_puppies > 0 for l in b.litters)
            ]

        # Sort results
        if sort_by == "award_score":
            results.sort(key=lambda b: b.award_score, reverse=True)
        elif sort_by == "champions":
            results.sort(key=lambda b: b.total_champions, reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda b: b.kennel_name.lower())

        return results

    def get_top_breeders(self, limit: int = 10) -> list[Breeder]:
        """Get top breeders ranked by AKC award score."""
        return self.search(sort_by="award_score")[:limit]

    def get_breeders_by_state(self, state: str) -> list[Breeder]:
        """Get all breeders in a specific state."""
        return self.search(state=state)

    def get_breeders_with_puppies(self) -> list[Breeder]:
        """Get breeders with currently available puppies."""
        return self.search(has_available_puppies=True)

    def get_elite_breeders(self) -> list[Breeder]:
        """Get breeders with Breeder of Merit + CHIC + RRCUS membership."""
        return self.search(
            require_breeder_of_merit=True,
            require_chic=True,
            require_rrcus=True
        )

    def get_all_states(self) -> list[str]:
        """Get list of all states with breeders."""
        states = set(b.state.upper() for b in self.breeders)
        return sorted(states)

    def get_statistics(self) -> dict:
        """Get statistics about the breeder database."""
        total_breeders = len(self.breeders)
        total_champions = sum(b.total_champions for b in self.breeders)
        bom_count = sum(1 for b in self.breeders if b.has_breeder_of_merit)
        chic_count = sum(1 for b in self.breeders if b.has_chic_dogs)
        rrcus_count = sum(1 for b in self.breeders if b.rrcus_member)
        states_count = len(self.get_all_states())

        return {
            "total_breeders": total_breeders,
            "total_champions": total_champions,
            "breeders_of_merit": bom_count,
            "chic_certified": chic_count,
            "rrcus_members": rrcus_count,
            "states_covered": states_count
        }
