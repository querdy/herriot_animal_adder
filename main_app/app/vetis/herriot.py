import datetime
import uuid

from loguru import logger
from zeep import xsd

from app.vetis.schemas.herriot import AnimalRegistration
from app.vetis.base import Base


def _push(method):
    def wrapper(self, *args, **kwargs):
        return self._push_request(method(self, *args, **kwargs))

    return wrapper


class Herriot(Base):
    def __init__(
            self,
            wsdl: str,
            enterprise_login: str,
            enterprise_password: str,
            api_key: str,
            service_id: str,
            issuer_id: str,
            initiator: str,
    ):
        self.wsdl = wsdl
        # self.wsdl = "https://api.vetrf.ru/schema/platform/herriot/v1.0b-last/ams-herriot.service_v1.0.wsdl"
        # self.port_address = "https://api2.vetrf.ru:8002/platform/services/2.1/ApplicationManagementService"
        self.port_address = "https://api.vetrf.ru/platform/services/2.1/ApplicationManagementService"
        self.api_key = api_key
        self.service_id = service_id
        self.issuer_id = issuer_id
        self.initiator = initiator
        self.enterprise_login = enterprise_login
        self.enterprise_password = enterprise_password
        self.last_application_id = None
        self.client = self._create_client(
            wsdl,
            self.enterprise_login,
            self.enterprise_password,
            port_address=self.port_address
        )
        self.factory = self._create_factory(self.client)

    def _push_request(self, application):
        request = self.client.service.submitApplicationRequest(
            apiKey=self.api_key,
            application=self.factory.ns3.Application(
                serviceId=self.service_id,
                issuerId=self.issuer_id,
                issueDate=datetime.datetime.now(),
                data=self.factory.ns3.ApplicationDataWrapper(_value_1=application),
            ),
        )
        # print(request)
        self.last_application_id = request.applicationId
        return request.applicationId

    def get_response(self, application_id: str = None):
        application_id = application_id or self.last_application_id
        response = self.client.service.receiveApplicationResult(
            apiKey=self.api_key, issuerId=self.issuer_id, applicationId=application_id
        )
        return response

    def get_finished_response(self, application_id: str = None):
        while True:
            response = self.get_response(application_id)
            if response.status == "IN_PROCESS":
                continue
            elif response.status == "REJECTED":
                return response
            else:
                return response

    @_push
    def get_animal_registration_changes_list(self,
                                             start_date: datetime.date,
                                             end_date: datetime.date,
                                             animal_species: str,
                                             keeping_place_guid: str = "",
                                             region_guid: str = '4f8b1a21-e4bb-422f-9087-d3cbf4bebc14',
                                             count: int = 100, offset: int = 0,
                                             local_transaction_id: str = uuid.uuid4()
                                             ):
        _element = self.client.get_element("ns5:getAnimalRegistrationChangesListRequest")
        application = xsd.AnyObject(
            _element,
            _element(
                localTransactionId=local_transaction_id,
                initiator=self.factory.ns8.User(login=self.initiator),
                listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
                updateDateInterval={
                    "beginDate": f"{start_date.isoformat()}T00:00:00",
                    "endDate": f"{end_date.isoformat()}T23:59:59",
                },
                region={
                    "guid": region_guid,
                },
                # operator={
                #     "guid": keeping_place_guid,
                # },
                animalSpecies={
                    "guid": animal_species,
                }
            ),
        )
        return application

    @_push
    def get_animal_registration_by_guid(
            self,
            guid: str,
            local_transaction_id: str = uuid.uuid4(),
    ):
        _element = self.client.get_element("ns5:getAnimalRegistrationByGuidRequest")
        application = xsd.AnyObject(
            _element,
            _element(
                localTransactionId=local_transaction_id,
                initiator=self.factory.ns8.User(login=self.initiator),
                animalRegistrationGuid=guid,
            ),
        )
        return application

    @_push
    def register_animal(self, animal_registration: AnimalRegistration, local_transaction_id: str = uuid.uuid4()):
        animal_registration = animal_registration.model_dump()
        if pedigree_info := animal_registration.get("pedigreeInfo"):
            edited_pedigree_info = {
                "parent": [
                    self.factory.ns8.AnimalRegistration(
                        guid=parent.get("guid"),
                        referencedDocument=parent.get("referencedDocument"))
                    for parent in pedigree_info["parent"]
                ]
            }
            animal_registration["pedigreeInfo"] = edited_pedigree_info
        _element = self.client.get_element("ns5:registerAnimalRequest")
        application = xsd.AnyObject(
            _element,
            _element(
                localTransactionId=local_transaction_id,
                initiator=self.factory.ns8.User(login=self.initiator),
                animalRegistration=animal_registration,
            ),
        )
        return application

