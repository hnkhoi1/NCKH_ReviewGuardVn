"""Input and normalized data schemas for ReviewGuard VN taxonomy v2.0."""
import sys
from pathlib import Path
# Tự động tìm và thêm thư mục 'src' vào sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from models.taxonomy import MainLabel, PatternAnalysisStatus, PatternRecord, SuspiciousSubtype


class ReviewSource(str, Enum):
    """Known corpus origins; UNKNOWN supports future sources without inventing provenance."""
    VISPAMREVIEWS = "vispamreviews"
    SELF_COLLECTED = "self_collected"
    UNKNOWN = "unknown"


class DataModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RawReviewRecord(DataModel):
    """Review as received from a source, before normalization or label mapping."""
    review_id: str = Field(min_length=1)
    review_text: str = ""
    star_rating: int | None = Field(default=None, ge=1, le=5)
    posted_at: datetime | None = None
    product_id: str | None = None
    seller_id: str | None = None
    reviewer_id_hash: str | None = None
    helpful_votes: int | None = Field(default=None, ge=0)
    
    has_media: bool | None = None
    review_image_uris: list[str] = Field(default_factory=list)
    seller_product_uris: list[str] = Field(default_factory=list)
    
    source: ReviewSource = ReviewSource.UNKNOWN
    source_dataset: str | None = None
    source_label: str | None = None

    @field_validator(
        "product_id", "seller_id", "reviewer_id_hash", "source_dataset", "source_label",
        mode="before",
    )
    @classmethod
    def blank_optional_strings_become_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def validate_media_consistency(self) -> "RawReviewRecord":
        if self.has_media and not self.review_image_uris:
            raise ValueError("has_media is True but review_image_uris is empty")
        return self


class NormalizedReviewRecord(DataModel):
    """Validated review retaining raw text alongside the model-ready representation."""
    review_id: str = Field(min_length=1)
    review_text_raw: str = ""
    review_text_normalized: str = ""
    star_rating: int | None = Field(default=None, ge=1, le=5)
    posted_at: datetime | None = None
    product_id: str | None = None
    seller_id: str | None = None
    reviewer_id_hash: str | None = None
    helpful_votes: int | None = Field(default=None, ge=0)
    
    has_media: bool | None = None
    review_image_uris: list[str] = Field(default_factory=list)
    seller_product_uris: list[str] = Field(default_factory=list)
    
    source: ReviewSource = ReviewSource.UNKNOWN
    source_dataset: str | None = None
    source_label: str | None = None


class SourceLabelMapping(DataModel):
    """Provenance-aware mapping from a dataset label to this project's taxonomy."""
    review_id: str = Field(min_length=1)
    source_dataset: str = Field(min_length=1)
    source_label: str = Field(min_length=1)
    mapped_main_label: MainLabel | None = None
    mapped_sub_labels: list[SuspiciousSubtype] = Field(default_factory=list)
    mapping_rule: str = Field(min_length=1)
    mapping_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    
    taxonomy_version: str = Field(default="v2.0", min_length=1)
    held_out: bool = False


class ReviewBatch(DataModel):
    """A batch with unique review IDs, useful at loader/API boundaries."""
    reviews: list[RawReviewRecord]

    @field_validator("reviews")
    @classmethod
    def review_ids_must_be_unique(cls, reviews: list[RawReviewRecord]) -> list[RawReviewRecord]:
        ids = [review.review_id for review in reviews]
        if len(ids) != len(set(ids)):
            raise ValueError("review_id values must be unique within a batch")
        return reviews


class PatternAnalysisResult(DataModel):
    """Result/status for analyzing a product or seller review set."""
    scope_type: str = Field(min_length=1)  # e.g. product or seller
    scope_id: str = Field(min_length=1)
    status: PatternAnalysisStatus
    patterns: list[PatternRecord] = Field(default_factory=list)
    message: str | None = None

    @field_validator("patterns")
    @classmethod
    def patterns_match_status(
        cls, patterns: list[PatternRecord], info
    ) -> list[PatternRecord]:
        status = info.data.get("status")
        if status == PatternAnalysisStatus.PATTERN_FOUND and not patterns:
            raise ValueError("pattern_found status requires at least one pattern")
        if status in {
            PatternAnalysisStatus.NO_PATTERN,
            PatternAnalysisStatus.NOT_ANALYZED,
            PatternAnalysisStatus.INSUFFICIENT_DATA,
        } and patterns:
            raise ValueError("patterns must be empty unless status is pattern_found")
        return patterns
