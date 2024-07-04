import typing

import zeep
from zeep import Client, Transport, Settings
from zeep.plugins import HistoryPlugin
from zeep.proxy import ServiceProxy

from app.vetis.shared.http_functions import http_login
from app.vetis.shared.type_factory import VetisFactory
from app.vetis.zeep_plugins.plugins import PatchXml

history = HistoryPlugin()


class VetisClient(Client):
    def __init__(
        self,
        wsdl,
        wsse=None,
        transport=None,
        service_name=None,
        port_name=None,
        plugins=None,
        settings=None,
        port_address=None,
    ):
        super().__init__(wsdl, wsse, transport, service_name, port_name, plugins, settings)
        self.port_address = port_address

    def bind(
        self,
        service_name: typing.Optional[str] = None,
        port_name: typing.Optional[str] = None,
    ):
        if not self.wsdl.services:
            return

        service = self._get_service(service_name)
        port = self._get_port(service, port_name)
        return ServiceProxy(self, port.binding, **port.binding_options)

    def _get_port(self, service, name):
        if name:
            port = service.ports.get(name)
            if not port:
                raise ValueError("Port not found")
        else:
            port = list(service.ports.values())[0]
        if self.port_address is not None:
            port.binding_options["address"] = self.port_address
        return port


class Base:
    @staticmethod
    def _create_client(
        wsdl: str, enterprise_login: str, enterprise_password: str, port_address: str = None
    ) -> zeep.client.Client:
        return VetisClient(
            wsdl=wsdl,
            port_address=port_address,
            settings=Settings(strict=False),
            transport=Transport(
                session=http_login(
                    enterprise_login=enterprise_login,
                    enterprise_password=enterprise_password,
                )
            ),
            plugins=[PatchXml(), history],
        )

    @staticmethod
    def _create_factory(client: zeep.client.Client) -> VetisFactory:
        return VetisFactory(client)
