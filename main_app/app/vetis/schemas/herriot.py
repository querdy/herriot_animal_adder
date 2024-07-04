import datetime
from enum import Enum
from typing import Optional, Literal, Any
from uuid import UUID

import typing_extensions
from openpyxl.descriptors.excel import Guid
from pydantic import field_serializer, Field, field_validator, model_validator

from app.vetis.schemas.base import CamelModel
from app.vetis.schemas.enums import *

IncEx: typing_extensions.TypeAlias = (
    "set[int] | set[str] | dict[int, Any] | dict[str, Any] | None"
)


class ComplexDate(CamelModel):
    year: str | int
    month: str | int
    day: Optional[str | int] = Field(default=None)


class ComplexDatePeriod(CamelModel):
    date: Optional[ComplexDate] = None
    start_date: Optional[ComplexDate] = None
    end_date: Optional[ComplexDate] = None

    @model_validator(mode="after")
    def check_date_or_start_date_and_end_date(self) -> "ComplexDatePeriod":
        if self.date is None and any([self.start_date is None, self.end_date is None]):
            raise ValueError(
                f"Необходимо указать `date` или `start_date` и `end_date`1"
            )
        elif self.date is not None and any(
            [self.start_date is not None, self.end_date is not None]
        ):
            raise ValueError(
                f"Необходимо указать `date` или `start_date` и `end_date`2"
            )
        return self


class GUID(CamelModel):
    guid: UUID

    @field_serializer("guid")
    def serialize_guid(self, field: UUID):
        return str(field)


class GUIDOrINN(CamelModel):
    guid: Optional[UUID] = Field(default=None)
    inn: Optional[str] = Field(default=None)

    @field_serializer("guid")
    def serialize_guid(self, field: UUID):
        return str(field)

    @model_validator(mode="after")
    def check_one(self) -> "GUIDOrINN":
        if (
            self.guid is None
            and self.inn is None
            or self.guid is not None
            and self.inn is not None
        ):
            raise ValueError(f"Необходимо указать `guid` или `inn`")
        return self


class SupervisedObject(CamelModel):
    supervised_object: GUID


class AssociatedMarkingEvent(CamelModel):
    type: VeterinaryEventType
    actual_date: ComplexDatePeriod
    operator_business_entity: Optional[GUIDOrINN] = Field(default=None)
    occurrence_reason: Optional[AnimalMarkingEventReason] = Field(default=None)

    @field_serializer(
        "type",
        "occurrence_reason",
    )
    def serialize_enum(self, field: Enum):
        return field.name

    @model_validator(mode="after")
    def check_occurrence_reason(self) -> "AssociatedMarkingEvent":
        if self.type == VeterinaryEventType.AIR and self.occurrence_reason is None:
            raise ValueError(
                f"Для {self.type.name} необходимо указать `occurrence_reason`"
            )
        return self


class AnimalMarkingMeans(CamelModel):
    type: MarkingMeansType

    @field_serializer(
        "type",
    )
    def serialize_enum(self, field: Enum):
        return field.name


class AnimalID(CamelModel):
    value_1: str = Field(alias="_value_1")
    format: AnimalIDFormat = Field(default=None)

    @field_serializer(
        "format",
    )
    def serialize_enum(self, field: Enum):
        return field.name


class AnimalLabel(CamelModel):
    type: AnimalLabelType
    marking_means: AnimalMarkingMeans
    attachment_location: GUID
    animal_id: Optional[AnimalID] = Field(default=None, alias="animalID")
    # animal_id: Optional[str] = Field(default=None, alias="animalID")
    description: Optional[str] = Field(default=None)

    @field_serializer(
        "type",
    )
    def serialize_enum(self, field: Enum):
        return field.name

    @model_validator(mode="after")
    def check_marking_means(self) -> "AttachedLabel":
        is_description = self.description is not None
        is_animal_id = self.animal_id is not None
        marking_means_name = self.marking_means.type.name

        if not any([is_description, is_animal_id]):
            raise ValueError(f"Необходимо указать `animal_id` или `description`")

        if marking_means_name in ("BRAND", "TATTOO", "TISSUE_SECTION"):
            if not is_description or is_animal_id:
                raise ValueError(
                    f"Для {marking_means_name} необходимо указать только `description`"
                )
        else:
            if is_description or not is_animal_id:
                raise ValueError(
                    f"Для {marking_means_name} необходимо указать только `animal_id_format` и `animal_id`"
                )
        return self


class ReferencedDocument(CamelModel):
    uuid: Optional[UUID] = None
    issue_number: Optional[str] = None
    type: Optional[str] = None
    relationship_type: str = "6"

    @field_serializer("uuid")
    def serialize_uuid(self, field: UUID):
        return str(field)

    @model_validator(mode="after")
    def check_identity(self) -> "ReferencedDocument":
        if all([self.uuid is None, self.issue_number is None]) or all(
            [self.uuid is not None, self.issue_number is not None]
        ):
            raise ValueError(f"Необходимо указать одно: `uuid` или `issue_number`")
        if self.type is None:
            if self.uuid is not None:
                self.type = "55"
            if self.issue_number is not None:
                self.type = "56"
        return self


class AnimalKeepingDetails(CamelModel):
    operator_supervised_object: GUID
    keeping_type: GUID
    keeping_purpose: list[GUID]

    @field_validator("keeping_purpose")
    def validate_specified_animal_identity(cls, value: list[GUID]) -> list[GUID]:
        if len(value) < 1:
            raise ValueError("Должен содержать хотя бы один элемент")
        return value


class AnimalColour(CamelModel):
    name: str


class SpecifiedAnimal(CamelModel):
    species: GUID
    gender: AnimalGender = Field(default=None)
    breed: Optional[GUID] = Field(default=None)
    colour: Optional[AnimalColour] = Field(default=None)
    name: Optional[str] = Field(default=None)
    birth_date: Optional[ComplexDate] = Field(default=None)
    birth_location: Optional[SupervisedObject] = Field(default=None)

    @field_serializer(
        "gender",
    )
    def serialize_enum(self, field: Enum):
        return field.name


class SpecifiedAnimalGroup(CamelModel):
    species: GUID
    breed: Optional[GUID] = Field(default=None)
    gender: AnimalGroupGender = Field(default=None)
    size: int
    birth_date_period: Optional[ComplexDatePeriod] = Field(default=None)

    @field_serializer(
        "gender",
    )
    def serialize_enum(self, field: Enum):
        return field.name


class SpecifiedAnimalIdentity(CamelModel):
    attached_label: AnimalLabel
    associated_marking_event: list[AssociatedMarkingEvent] = Field(default=None)


class PedigreeParent(CamelModel):
    guid: Optional[UUID] = Field(default=None)
    referenced_document: ReferencedDocument = Field(default=None)

    @model_validator(mode="after")
    def check_one(self) -> "PedigreeParent":
        if (
            self.guid is None
            and self.referenced_document is None
            or self.guid is not None
            and self.referenced_document is not None
        ):
            raise ValueError(f"Необходимо указать `guid` или `referenced_document`")
        return self

    @field_serializer("guid")
    def serialize_guid(self, field: UUID):
        return str(field)


class AnimalPedigreeInfo(CamelModel):
    parent: list[PedigreeParent]

    @field_validator("parent")
    def validate_specified_animal_identity(
        cls, value: list[PedigreeParent]
    ) -> list[PedigreeParent]:
        if len(value) < 1 or len(value) > 2:
            raise ValueError("Должен содержать один или два элемента")
        return value


class AnimalRegistration(CamelModel):
    identity_type: IdentityType
    registration_status: RegistrationStatus = Field(default=RegistrationStatus.ACTIVE)
    initial_identification_type: InitialIdentificationType
    breeding_value_type: AnimalBreedingValueType
    specified_animal_identity: list[SpecifiedAnimalIdentity]
    specified_animal: Optional[SpecifiedAnimal] = Field(default=None)
    specified_animal_group: Optional[SpecifiedAnimalGroup] = Field(default=None)
    keeping_details: AnimalKeepingDetails
    referenced_document: ReferencedDocument
    pedigree_info: Optional[AnimalPedigreeInfo] = Field(default=None)
    guid: Optional[str] = Field(default=None)
    registration_number: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def check_model(self) -> "AnimalRegistration":
        if self.identity_type == IdentityType.INDIVIDUAL:
            if (
                self.specified_animal is None
                and self.specified_animal_group is not None
            ):
                raise ValueError(
                    f"Для {self.identity_type} необходимо указать `specified_animal`"
                )
        else:
            if (
                self.specified_animal is not None
                and self.specified_animal_group is None
            ):
                raise ValueError(
                    f"Для {self.identity_type} необходимо указать `specified_animal_group`"
                )

        if self.initial_identification_type == InitialIdentificationType.BIRTH:
            if self.pedigree_info is None:
                raise ValueError(
                    f"Для {self.initial_identification_type} необходимо указать `pedigree_info`"
                )
        return self

    @field_validator("specified_animal_identity")
    def validate_specified_animal_identity(
        cls, value: list[SpecifiedAnimalIdentity]
    ) -> list[SpecifiedAnimalIdentity]:
        if len(value) < 1:
            raise ValueError("Должен содержать хотя бы один элемент")
        return value

    @field_serializer(
        "identity_type",
        "breeding_value_type",
        "registration_status",
        "initial_identification_type",
    )
    def serialize_enum(self, field: Enum):
        return field.name
