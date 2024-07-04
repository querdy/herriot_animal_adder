from PyQt6.QtCore import QMutex

from app.vetis.dictionary_service import DictionaryService
from app.vetis.enterprise_service import EnterpriseService
from app.vetis.herriot import Herriot


class VetisMeta(type):
    _api_key = None
    _service_id = None
    _issuer_id = None
    _enterprise_login = None
    _enterprise_password = None
    _initiator = None
    _wsdl_herriot = None
    _wsdl_dictionary_service = None
    _wsdl_enterprise_service = None
    _herriot = None
    _dictionary_service = None
    _enterprise_service = None

    _mutex_herriot = QMutex()
    _mutex_dictionary_service = QMutex()
    _mutex_enterprise_service = QMutex()

    @property
    def initialized(cls) -> bool:
        return not any(
            item is None
            for item in [
                cls._api_key,
                cls._service_id,
                cls._issuer_id,
                cls._enterprise_login,
                cls._enterprise_password,
                cls._initiator,
                cls._wsdl_herriot,
                cls._wsdl_dictionary_service,
                cls._wsdl_enterprise_service,
            ]
        )

    @property
    def herriot(cls) -> Herriot:
        cls._mutex_herriot.lock()
        if cls._herriot is None:
            assert cls.initialized, "Vetis not initialized"
            cls._herriot = Herriot(
                cls._wsdl_herriot,
                cls._enterprise_login,
                cls._enterprise_password,
                cls._api_key,
                cls._service_id,
                cls._issuer_id,
                cls._initiator,
            )
        cls._mutex_herriot.unlock()
        return cls._herriot

    @property
    def enterprise_service(cls) -> EnterpriseService:
        cls._mutex_enterprise_service.lock()
        if cls._enterprise_service is None:
            assert cls.initialized, "Vetis not initialized"
            cls._enterprise_service = EnterpriseService(
                cls._wsdl_enterprise_service,
                cls._enterprise_login,
                cls._enterprise_password,
            )
        cls._mutex_enterprise_service.unlock()
        return cls._enterprise_service

    @property
    def dictionary_service(cls) -> DictionaryService:
        cls._mutex_dictionary_service.lock()
        if cls._dictionary_service is None:
            assert cls.initialized, "Vetis not initialized"
            cls._dictionary_service = DictionaryService(
                cls._wsdl_dictionary_service,
                cls._enterprise_login,
                cls._enterprise_password,
            )
        cls._mutex_dictionary_service.unlock()
        return cls._dictionary_service


class Vetis(metaclass=VetisMeta):
    @classmethod
    def initialize(
        cls,
        api_key: str,
        service_id: str,
        issuer_id: str,
        enterprise_login: str,
        enterprise_password: str,
        initiator: str,
        wsdl_herriot: str,
        wsdl_dictionary_service: str,
        wsdl_enterprise_service: str,
    ) -> None:
        cls._api_key = api_key
        cls._service_id = service_id
        cls._issuer_id = issuer_id
        cls._enterprise_login = enterprise_login
        cls._enterprise_password = enterprise_password
        cls._initiator = initiator
        cls._wsdl_herriot = wsdl_herriot
        cls._wsdl_dictionary_service = wsdl_dictionary_service
        cls._wsdl_enterprise_service = wsdl_enterprise_service

        cls._herriot = None
        cls._dictionary_service = None
        cls._enterprise_service = None

    @classmethod
    def switch_initiator(cls, initiator: str) -> None:
        cls._initiator = initiator
        cls._herriot = None

    @classmethod
    def initiator(cls) -> str:
        return cls._initiator
