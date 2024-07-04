from functools import lru_cache

from loguru import logger

# import xmltodict

from app.vetis.base import Base


class EnterpriseService(Base):
    def __init__(
        self,
        wsdl: str,
        enterprise_login: str,
        enterprise_password: str,
    ):
        self.wsdl = wsdl
        # self.wsdl = "https://api.vetrf.ru/schema/platform/herriot/v1.0b-last/EnterpriseService_v1.0.wsdl"
        # self.port_address = "https://api2.vetrf.ru:8002/platform/herriot/services/1.0/EnterpriseService"
        self.port_address = "https://api.vetrf.ru/platform/herriot/services/1.0/EnterpriseService"
        self.enterprise_login = enterprise_login
        self.enterprise_password = enterprise_password
        self.client = self._create_client(
            wsdl,
            enterprise_login,
            enterprise_password,
            port_address=self.port_address
        )
        self.factory = self._create_factory(self.client)

    @lru_cache(maxsize=8)
    def get_be_supervised_object_list(
        self,
        inn: str = None,
        guid: str = None,
        approval_number: str = None,
        count: int = 1000,
        offset: int = 0,
    ):
        response = self.client.service.GetBESupervisedObjectList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            businessEntity=self.factory.ns4.BusinessEntity(inn=inn, guid=guid),
            supervisedObject=self.factory.ns4.SupervisedObject(
                approvalNumber=approval_number
            ),
        )
        # print(response)
        # pprint(serialize_object(response, dict))
        return response["supervisedObject"]

    @lru_cache(maxsize=8)
    def get_be_business_entity_list(
        self, inn: str = None, guid: str = None, count: int = 1000, offset: int = 0
    ):
        response = self.client.service.GetBusinessEntityList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            businessEntity=self.factory.ns4.BusinessEntity(inn=inn, guid=guid),
        )
        # pprint(serialize_object(response, dict))
        return response

    @lru_cache(maxsize=8)
    def get_business_entity_list(self, inn: str, count: int = 1000, offset: int = 0):
        response = self.client.service.GetBusinessEntityList(
            listOptions=self.factory.ns1.ListOptions(count=count, offset=offset),
            businessEntity=self.factory.ns4.BusinessEntity(inn=inn),
        )
        # pprint(serialize_object(response, dict))
        return response

    @lru_cache(maxsize=8)
    def get_supervised_object_by_guid(self, guid: str):
        response = self.client.service.GetSupervisedObjectByGuid(guid=guid)
        # pprint(serialize_object(response, dict))
        return response

    @lru_cache(maxsize=8)
    def get_enterprise_by_guid(self, guid: str):
        response = self.client.service.GetEnterpriseByGuid(guid=guid)
        # pprint(serialize_object(response, dict))
        return response
