import os
from functools import lru_cache

import pandas as pd
from loguru import logger

from app.vetis.schemas.enums import (
    AnimalGender,
    AnimalBreedingValueType,
    InitialIdentificationType,
    AnimalLabelType,
    MarkingMeansType,
)


def close_excel():
    processes = ('excel.exe', 'EXCEL.EXE', 'excel.EXE', 'EXCEL.exe')
    for process in processes:
        os.system("chcp 65001 > nul")
        os.system(f"taskkill /f /im {process}")


def check_species(species: str, specieses: list) -> bool:
    for item in specieses:
        if item.name == species:
            return True
    return False


def get_species(species: str, specieses: list):
    for item in specieses:
        if item.name == species:
            return item.guid


def get_species_name_by_guid(species: str, specieses: list):
    for item in specieses:
        if item["guid"] == species:
            return item.name


def check_breed(breed: str, species: str, breeds: list) -> bool:
    if pd.isna(breed):
        return True
    for item in breeds:
        if item.name == breed and item.species.name == species:
            return True


def get_breed(breed: str, species: str, breeds: list):
    for item in breeds:
        if item.name == breed and item.species.name == species:
            return item.guid


def check_keeping_type(keeping_type: str, keeping_types: list) -> bool:
    for item in keeping_types:
        if item.name == keeping_type:
            return True
    return False


def get_keeping_type(keeping_type: str, keeping_types: list):
    for item in keeping_types:
        if item.name == keeping_type:
            return item.guid


def check_marking_location(marking_location: str, marking_locations: list) -> bool:
    if pd.isna(marking_location):
        return True
    for item in marking_locations:
        if item.name == marking_location:
            return True


def get_marking_location(marking_location: str, marking_locations: list):
    for item in marking_locations:
        if item.name == marking_location:
            return item.guid


def check_keeping_purpose(keeping_purpose: str, keeping_purposes: list) -> bool:
    for item in keeping_purposes:
        if item.name == keeping_purpose:
            return True
    return False


def get_keeping_purpose(keeping_purpose: str, keeping_purposes: list):
    for item in keeping_purposes:
        if item.name == keeping_purpose:
            return item.guid


def get_supervised_object(supervised_object: str, supervised_objects: list):
    for item in supervised_objects:
        if item.approvalNumber == supervised_object:
            return item


def check_supervised_object(supervised_object: str, supervised_objects: list):
    for item in supervised_objects:
        if item.approvalNumber == supervised_object:
            return True
    return False


def check_keeping_place_allowed(keeping_place, allowed_districts: list[str]):
    if keeping_place.enterprise.address.district is None:
        return keeping_place.enterprise.address.locality.guid in allowed_districts
    else:
        return keeping_place.enterprise.address.district.guid in allowed_districts


def check_animal_gender(gender: str) -> bool:
    try:
        AnimalGender(gender)
        return True
    except ValueError:
        return False


def check_breeding_value(breeding_value: str) -> bool:
    try:
        AnimalBreedingValueType(breeding_value)
        return True
    except ValueError:
        return False


def check_initial_identification(initial_identification: str) -> bool:
    try:
        InitialIdentificationType(initial_identification)
        return True
    except ValueError:
        return False


def check_label_type(label_type: str) -> bool:
    try:
        AnimalLabelType(label_type)
        return True
    except ValueError:
        return False


def check_marking_means(marking_means: list) -> bool:
    if pd.isna(marking_means):
        return True
    try:
        MarkingMeansType(marking_means)
        return True
    except ValueError:
        return False


def check_label_id(label_id: str, label_type: str) -> bool:
    if pd.isna(label_id):
        return True
    try:
        label_type = AnimalLabelType(label_type)
    except ValueError:
        label_type = AnimalLabelType.ADDITIONAL
    finally:
        if label_type == AnimalLabelType.MAIN:
            # ToDo проверка формата основного средства маркирования
            return True
        else:
            return True
