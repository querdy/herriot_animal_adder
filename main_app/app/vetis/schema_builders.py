import datetime
import uuid
from pprint import pprint
from typing import Literal
from uuid import UUID, uuid4

from app.vetis.schemas.enums import *

from app.vetis.schemas.enums import (
    InitialIdentificationType,
    AnimalGender,
    AnimalLabelType,
    MarkingMeansType,
    AnimalIDFormat,
    RegistrationStatus,
    AnimalBreedingValueType,
    IdentityType,
    VeterinaryEventType,
)
from app.vetis.schemas.herriot import (
    AssociatedMarkingEvent,
    ComplexDatePeriod,
    GUIDOrINN,
    ReferencedDocument,
    AnimalKeepingDetails,
    SpecifiedAnimalIdentity,
    AnimalLabel,
    AnimalMarkingMeans,
    AnimalID,
    SpecifiedAnimal,
    GUID,
    AnimalColour,
    ComplexDate,
    SupervisedObject,
    AnimalRegistration,
    SpecifiedAnimalGroup,
    AnimalPedigreeInfo, PedigreeParent,
)

f = AssociatedMarkingEvent(
    type=VeterinaryEventType.AME,
    actual_date=ComplexDatePeriod(date={"year": 2020, "month": 7, "day": 5}),
    operator_business_entity=GUIDOrINN(inn="5948026633"),
)

# g = AssociatedMarkingEvent(
#     type=VeterinaryEventType.AIR,
#     actual_date=ComplexDatePeriod(date={"year": 2021, "month": 1, "day": 1}),
#     operator_business_entity=GUIDOrINN(inn="5948026633"),
#     occurrence_reason=AnimalMarkingEventReason.LOSS
# )

e = ReferencedDocument(
    uuid=uuid4(),
)

d = AnimalKeepingDetails(
    operator_supervised_object=GUID(guid="50312f1b-00e2-4458-afa6-feb4426566c4"),
    keeping_type=GUID(guid="99e904cc-a48c-438f-86b4-3f5e28dbd07c"),
    keeping_purpose=[
        GUID(guid="b8c2917d-dcc8-489a-803a-eeecb4822cb9"),
    ],
)

c = SpecifiedAnimalIdentity(
    attached_label=AnimalLabel(
        type=AnimalLabelType.ADDITIONAL,
        marking_means=AnimalMarkingMeans(type=MarkingMeansType.LABEL),
        attachment_location=GUID(guid="19b45434-1c0c-a2dd-ade7-9e0cb767a28c"),
        animal_id=AnimalID(
            value_1=f"{int(datetime.datetime.now().timestamp())}",
            format=AnimalIDFormat.OTHER,
        ),
        # description="registred_animals"
    ),
    associated_marking_event=[
        f,
    ],
)

b = SpecifiedAnimal(
    species=GUID(guid=UUID("a4588321-f300-4c85-840b-9414c371addd")),
    gender=AnimalGender.FEMALE,
    breed=GUID(guid="63a1430d-d50f-45b3-9728-0d4097939443"),
    colour=AnimalColour(name="черно-пестрая"),
    name=f"Буренка {int(datetime.datetime.now().timestamp())}",
    birth_date=ComplexDate(year=2020, month=4, day=5),
    birth_location=SupervisedObject(
        supervised_object=GUID(guid="50312f1b-00e2-4458-afa6-feb4426566c4")
    ),
)

a = AnimalRegistration(
    identity_type=IdentityType.INDIVIDUAL,
    registration_status=RegistrationStatus.ACTIVE,
    initial_identification_type=InitialIdentificationType.OTHER,
    breeding_value_type=AnimalBreedingValueType.BREEDING,
    specified_animal=b,
    specified_animal_identity=[
        c,
    ],
    keeping_details=d,
    referenced_document=e,
)


def build_referenced_document(
        uuid: UUID = None,
        issue_number: str = None,
        type: str = None,
        relationship_type: str = "6",
) -> ReferencedDocument:
    return ReferencedDocument(
        uuid=uuid,
        issue_number=issue_number,
        type=type,
        relationship_type=relationship_type,
    )


def build_associated_marking_event(
        type: VeterinaryEventType,
        actual_date: ComplexDate,
        operator_business_entity: GUIDOrINN,
) -> AssociatedMarkingEvent:
    return AssociatedMarkingEvent(
        type=type,
        actual_date=ComplexDatePeriod(date=actual_date),
        operator_business_entity=operator_business_entity,
    )


def build_animal_keeping_detail(
        operator_supervised_object: UUID, keeping_type: UUID, keeping_purpose: list[UUID]
) -> AnimalKeepingDetails:
    return AnimalKeepingDetails(
        operator_supervised_object=GUID(guid=operator_supervised_object),
        keeping_type=GUID(guid=keeping_type),
        keeping_purpose=[GUID(guid=purpose) for purpose in keeping_purpose],
    )


def build_ame_specified_animal_identity(
        type: AnimalLabelType,
        marking_means: MarkingMeansType,
        attachment_location: UUID,
        actual_date: ComplexDate,
        operator_business_entity: GUIDOrINN = None,
        description: str = None,
        animal_id: str = None,
        animal_id_format: AnimalIDFormat = AnimalIDFormat.OTHER,
) -> SpecifiedAnimalIdentity:
    return SpecifiedAnimalIdentity(
        attached_label=AnimalLabel(
            type=type,
            marking_means=AnimalMarkingMeans(type=marking_means),
            attachment_location=GUID(guid=attachment_location),
            animal_id=AnimalID(value_1=animal_id, format=animal_id_format),
            description=description,
        ),
        associated_marking_event=[
            AssociatedMarkingEvent(
                type=VeterinaryEventType.AME,
                actual_date=ComplexDatePeriod(date=actual_date),
                operator_business_entity=operator_business_entity,
            )
        ],
    )


def build_air_specified_animal_identity() -> SpecifiedAnimalIdentity:
    raise NotImplementedError


def build_specified_animal(
        species: UUID,
        gender: AnimalGender,
        birth_location: UUID = None,
        birth_date: ComplexDate = None,
        breed: UUID = None,
        colour: str = None,
        name: str = None,
) -> SpecifiedAnimal:
    return SpecifiedAnimal(
        species=GUID(guid=species),
        gender=gender,
        breed=GUID(guid=breed) if breed else None,
        colour=AnimalColour(name=colour) if colour else None,
        name=name,
        birth_date=birth_date,
        birth_location=SupervisedObject(supervised_object=GUID(guid=birth_location)) if birth_location else None,
    )


def build_specified_animal_group(
        species: UUID,
        gender: AnimalGroupGender,
        size: int,
        start_birth_date_period: ComplexDate,
        end_birth_date_period: ComplexDate,
        breed: UUID = None,
) -> SpecifiedAnimalGroup:
    return SpecifiedAnimalGroup(
        species=GUID(guid=species),
        gender=gender,
        breed=GUID(guid=breed),
        size=size,
        birth_date_period=ComplexDatePeriod(
            start_date=start_birth_date_period, end_date=end_birth_date_period
        ),
    )


def build_pedigree_info(
        pedigree_info_herriot: list[str] = None, pedigree_info_external: list[str] = None
) -> AnimalPedigreeInfo:
    if pedigree_info_external is None and pedigree_info_herriot is not None:
        return AnimalPedigreeInfo(
            parent=[
                PedigreeParent(guid=UUID(animal)) for animal in pedigree_info_herriot
            ]
        )
    elif pedigree_info_herriot is None and pedigree_info_external is not None:
        return AnimalPedigreeInfo(
            parent=[
                PedigreeParent(referenced_document=ReferencedDocument(uuid=uuid.uuid5(uuid.NAMESPACE_DNS, animal)))
                for animal in pedigree_info_external
            ]
        )
    elif all([pedigree_info_herriot is not None, pedigree_info_external is not None]):
        raise ValueError(
            f"Необходимо указать что-то одно: `pedigree_info_herriot` или `pedigree_info_external`"
        )


def build_animal_registration(
        identity_type: IdentityType,
        initial_identification_type: InitialIdentificationType,
        breeding_value_type: AnimalBreedingValueType,
        specified_animal_identity: list[SpecifiedAnimalIdentity],
        keeping_details: AnimalKeepingDetails,
        referenced_document: ReferencedDocument,
        specified_animal: SpecifiedAnimal = None,
        specified_animal_group: SpecifiedAnimalGroup = None,
        registration_status: RegistrationStatus = RegistrationStatus.ACTIVE,
        pedigree_info: AnimalPedigreeInfo = None,
):
    animal_registration = {
        "identity_type": identity_type,
        "registration_status": registration_status,
        "initial_identification_type": initial_identification_type,
        "breeding_value_type": breeding_value_type,
        "specified_animal_identity": specified_animal_identity,
        "keeping_details": keeping_details,
        "referenced_document": referenced_document,
        "pedigree_info": pedigree_info,
    }

    match identity_type:
        case IdentityType.INDIVIDUAL:
            animal_registration.update({"specified_animal": specified_animal})
        case IdentityType.GROUP:
            animal_registration.update(
                {"specified_animal_group": specified_animal_group}
            )

    return AnimalRegistration(**animal_registration)


def get_animal_registration_ame_single(
        initial_identification_type: InitialIdentificationType,
        breeding_value_type: AnimalBreedingValueType,
        keeping_operator_supervised_object: str,
        keeping_type: str,
        keeping_purpose: list[str],
        species: str,
        gender: AnimalGender,
        birth_location: str = None,
        birth_date: ComplexDate = None,

        marking_means_main: MarkingMeansType = None,
        attachment_location_main: str = None,
        actual_date_main: ComplexDate = None,
        animal_id_main: str = None,

        marking_means_additional_1: MarkingMeansType = None,
        attachment_location_additional_1: str = None,
        actual_date_additional_1: ComplexDate = None,
        animal_id_additional_1: str = None,

        marking_means_additional_2: MarkingMeansType = None,
        attachment_location_additional_2: str = None,
        actual_date_additional_2: ComplexDate = None,
        animal_id_additional_2: str = None,

        ref_doc_uuid: str = None,
        ref_doc_issue_number: str = None,
        ref_doc_type: str = None,
        relationship_type: str = "6",
        breed: str = None,
        colour: str = None,
        name: str = None,
        registration_status: RegistrationStatus = RegistrationStatus.ACTIVE,
        pedigree_info_herriot: list[str] = None,
        pedigree_info_external: list[str] = None,
) -> AnimalRegistration:
    specified_animal_identity = []
    if all([marking_means_main, attachment_location_main, actual_date_main, animal_id_main]):
        specified_animal_identity.append(build_ame_specified_animal_identity(
            type=AnimalLabelType.MAIN,
            marking_means=marking_means_main,
            attachment_location=UUID(attachment_location_main),
            actual_date=actual_date_main,
            animal_id=animal_id_main,
            animal_id_format=AnimalIDFormat.UNMM,
        ))
    if all([marking_means_additional_1, attachment_location_additional_1, actual_date_additional_1, animal_id_additional_1]):
        specified_animal_identity.append(build_ame_specified_animal_identity(
            type=AnimalLabelType.ADDITIONAL,
            marking_means=marking_means_additional_1,
            attachment_location=UUID(attachment_location_additional_1),
            actual_date=actual_date_additional_1,
            animal_id=animal_id_additional_1,
            animal_id_format=AnimalIDFormat.OTHER,
        ))
    if all([marking_means_additional_2, attachment_location_additional_2, actual_date_additional_2, animal_id_additional_2]):
        specified_animal_identity.append(build_ame_specified_animal_identity(
            type=AnimalLabelType.ADDITIONAL,
            marking_means=marking_means_additional_2,
            attachment_location=UUID(attachment_location_additional_2),
            actual_date=actual_date_additional_2,
            animal_id=animal_id_additional_2,
            animal_id_format=AnimalIDFormat.OTHER,
        ))
    keeping_details = build_animal_keeping_detail(
        operator_supervised_object=UUID(keeping_operator_supervised_object),
        keeping_type=UUID(keeping_type),
        keeping_purpose=[UUID(purpose) for purpose in keeping_purpose],
    )
    referenced_document = build_referenced_document(
        uuid=uuid.uuid5(uuid.NAMESPACE_DNS, ref_doc_uuid),
        issue_number=ref_doc_issue_number,
        type=ref_doc_type,
        relationship_type=relationship_type,
    )
    specified_animal = build_specified_animal(
        species=UUID(species),
        gender=gender,
        birth_date=birth_date,
        birth_location=UUID(birth_location) if birth_location else None,
        breed=UUID(breed) if breed else None,
        colour=colour,
        name=name,
    )
    pedigree_info = build_pedigree_info(
        pedigree_info_herriot=pedigree_info_herriot,
        pedigree_info_external=pedigree_info_external,
    )
    animal_registration = build_animal_registration(
        identity_type=IdentityType.INDIVIDUAL,
        initial_identification_type=initial_identification_type,
        breeding_value_type=breeding_value_type,
        specified_animal_identity=specified_animal_identity,
        keeping_details=keeping_details,
        referenced_document=referenced_document,
        specified_animal=specified_animal,
        registration_status=registration_status,
        pedigree_info=pedigree_info,
    )
    return animal_registration


def get_animal_registration_ame_group(
        initial_identification_type: InitialIdentificationType,
        breeding_value_type: AnimalBreedingValueType,
        keeping_operator_supervised_object: str,
        keeping_type: str,
        keeping_purpose: list[str],
        species: str,
        gender: AnimalGroupGender,
        size: int,
        start_birth_date_period: ComplexDate,
        end_birth_date_period: ComplexDate,
        animal_label_type: AnimalLabelType,
        marking_means: MarkingMeansType,
        attachment_location: str,
        actual_date: ComplexDate,
        label_operator_business_entity: GUIDOrINN,
        description: str = None,
        animal_id: str = None,
        animal_id_format: AnimalIDFormat = AnimalIDFormat.OTHER,
        ref_doc_uuid: str = None,
        ref_doc_issue_number: str = None,
        ref_doc_type: str = None,
        relationship_type: str = "6",
        breed: str = None,
        registration_status: RegistrationStatus = RegistrationStatus.ACTIVE,
) -> AnimalRegistration:
    specified_animal_identity = build_ame_specified_animal_identity(
        type=animal_label_type,
        marking_means=marking_means,
        attachment_location=UUID(attachment_location),
        actual_date=actual_date,
        operator_business_entity=label_operator_business_entity,
        description=description,
        animal_id=animal_id,
        animal_id_format=animal_id_format,
    )
    keeping_details = build_animal_keeping_detail(
        operator_supervised_object=UUID(keeping_operator_supervised_object),
        keeping_type=UUID(keeping_type),
        keeping_purpose=[UUID(purpose) for purpose in keeping_purpose],
    )
    referenced_document = build_referenced_document(
        uuid=UUID(ref_doc_uuid),
        issue_number=ref_doc_issue_number,
        type=ref_doc_type,
        relationship_type=relationship_type,
    )
    specified_animal_group = build_specified_animal_group(
        species=UUID(species),
        gender=gender,
        breed=breed,
        size=size,
        start_birth_date_period=start_birth_date_period,
        end_birth_date_period=end_birth_date_period,
    )
    animal_registration = build_animal_registration(
        identity_type=IdentityType.GROUP,
        initial_identification_type=initial_identification_type,
        breeding_value_type=breeding_value_type,
        specified_animal_identity=[
            specified_animal_identity,
        ],
        keeping_details=keeping_details,
        referenced_document=referenced_document,
        specified_animal_group=specified_animal_group,
        registration_status=registration_status,
    )
    return animal_registration

