from datetime import datetime
from pprint import pprint

from zeep.helpers import serialize_object

from app.vetis.base import Base


class DictionaryService(Base):
    def __init__(
        self,
        wsdl: str,
        enterprise_login: str,
        enterprise_password: str,
    ):
        self.wsdl = wsdl
        # self.wsdl = "https://api.vetrf.ru/schema/platform/herriot/v1.0b-last/DictionaryService_v1.0.wsdl"
        # self.port_address = "https://api2.vetrf.ru:8002/platform/herriot/services/1.0/DictionaryService"
        self.port_address = "https://api.vetrf.ru/platform/herriot/services/1.0/DictionaryService"
        self.enterprise_login = enterprise_login
        self.enterprise_password = enterprise_password
        self.client = self._create_client(
            self.wsdl,
            self.enterprise_login,
            self.enterprise_password,
            port_address=self.port_address
        )
        self.factory = self._create_factory(self.client)

    def get_animal_breed_list(
        self,
        species_guid: str = None,
        count: int = 1000,
        offset: int = 0,
        name: str = "",
    ):
        if species_guid is None:
            response = self.client.service.GetAnimalBreedList(
                listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
                animalBreed=self.factory.ns4.AnimalBreed(
                    name=name,
                ),
            )
        else:
            response = self.client.service.GetAnimalBreedList(
                listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
                animalBreed=self.factory.ns4.AnimalBreed(
                    name=name, species=self.factory.ns4.AnimalSpecies(guid=species_guid)
                ),
            )
        # pprint(serialize_object(response, dict))
        return response["animalBreed"]

    def get_animal_species_list(
        self, count: int = 1000, offset: int = 0, name: str = "", code: str = ""
    ):
        response = self.client.service.GetAnimalSpeciesList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            animalSpecies=self.factory.ns4.AnimalSpecies(name=name, code=code),
        )
        # pprint(serialize_object(response, dict))
        return response["animalSpecies"]

    def get_animal_keeping_type_list(
        self, count: int = 1000, offset: int = 0, name: str = ""
    ):
        response = self.client.service.GetAnimalKeepingTypeList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            animalKeepingType=self.factory.ns4.AnimalKeepingType(name=name),
        )
        # pprint(serialize_object(response, dict))
        return response["animalKeepingType"]

    def get_animal_keeping_purpose_list(
        self, count: int = 1000, offset: int = 0, name: str = ""
    ):
        response = self.client.service.GetAnimalKeepingPurposeList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            animalKeepingPurpose=self.factory.ns4.AnimalKeepingPurpose(name=name),
        )
        # pprint(serialize_object(response, dict))
        return response["animalKeepingPurpose"]

    def get_animal_marking_location_list(self, count: int = 1000, offset: int = 0):
        response = self.client.service.GetAnimalMarkingLocationList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
        )
        # pprint(serialize_object(response, dict))
        return response["animalMarkingLocation"]

    def get_unit_list(self, count: int = 1000, offset: int = 0):
        response = self.client.service.GetUnitList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
        )
        # pprint(serialize_object(response, dict))
        return response
