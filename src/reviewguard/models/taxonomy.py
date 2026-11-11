"""Canonical labels and annotation models for ReviewGuard VN taxonomy v2.0."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MainLabel(str, Enum):
    TRUSTWORTHY = "trustworthy"
    SUSPICIOUS = "suspicious"
    UNCERTAIN = "uncertain"


class SuspiciousSubtype(str, Enum):
    DECEPTIVE_FAKE = "deceptive_fake"
    SPAM_ADVERTISING = "spam_advertising"
    OFF_TOPIC = "off_topic"
    MISLEADING_MANIPULATIVE = "misleading_manipulative"
    MEDIA_PRODUCT_MISMATCH = "media_product_mismatch"
    AI_GENERATED = "ai_generated"
    POOR_CONTENT = "poor_content"


class ImageComparisonStatus(str, Enum):
    NOT_CHECKED = "not_checked"
    NO_REVIEW_IMAGE = "no_review_image"
    NO_SELLER_REFERENCE = "no_seller_reference"
    COMPATIBLE = "compatible"
    MISMATCH_CANDIDATE = "mismatch_candidate"
    UNCERTAIN = "uncertain"
    PROCESSING_ERROR = "processing_error"


class PatternType(str, Enum):
    NEAR_DUPLICATE_CLUSTER = "near_duplicate_cluster"
    TIME_BURST = "time_burst"
    COORDINATED_GROUP = "coordinated_group"


class PatternAnalysisStatus(str, Enum):
    NOT_ANALYZED = "not_analyzed"
    NO_PATTERN = "no_pattern"
    PATTERN_FOUND = "pattern_found"
    INSUFFICIENT_DATA = "insufficient_data"


class TaxonomyModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ReviewAnnotation(TaxonomyModel):
    annotation_id: str = Field(min_length=1)
    review_id: str = Field(min_length=1)
    main_label: MainLabel
    sub_labels: list[SuspiciousSubtype] = Field(default_factory=list)
    image_status: ImageComparisonStatus = ImageComparisonStatus.NOT_CHECKED
    annotator_id: str = Field(min_length=1)
    guideline_version: str = Field(min_length=1, default="v2.0")
    annotator_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_label_consistency(self) -> "ReviewAnnotation":
        if self.main_label == MainLabel.SUSPICIOUS and not self.sub_labels:
            raise ValueError("suspicious annotations require at least one subtype")
        if self.main_label != MainLabel.SUSPICIOUS and self.sub_labels:
            raise ValueError("sub_labels are only valid when main_label is suspicious")
        if len(self.sub_labels) != len(set(self.sub_labels)):
            raise ValueError("sub_labels must not contain duplicates")
        return self


class AdjudicatedLabel(TaxonomyModel):
    review_id: str = Field(min_length=1)
    main_label: MainLabel
    sub_labels: list[SuspiciousSubtype] = Field(default_factory=list)
    adjudicator_id: str = Field(min_length=1)
    guideline_version: str = Field(min_length=1, default="v2.0")
    notes: str | None = None

    @model_validator(mode="after")
    def validate_label_consistency(self) -> "AdjudicatedLabel":
        if self.main_label == MainLabel.SUSPICIOUS and not self.sub_labels:
            raise ValueError("suspicious adjudications require at least one subtype")
        if self.main_label != MainLabel.SUSPICIOUS and self.sub_labels:
            raise ValueError("sub_labels are only valid when main_label is suspicious")
        if len(self.sub_labels) != len(set(self.sub_labels)):
            raise ValueError("sub_labels must not contain duplicates")
        return self


class PatternRecord(TaxonomyModel):
    pattern_id: str = Field(min_length=1)
    pattern_type: PatternType
    member_review_ids: list[str] = Field(min_length=2)
    method: str = Field(min_length=1)
    method_version: str = Field(min_length=1)
    score: float | None = None
    evidence: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_members(self) -> "PatternRecord":
        if len(self.member_review_ids) != len(set(self.member_review_ids)):
            raise ValueError("member_review_ids must be unique")
        return self
