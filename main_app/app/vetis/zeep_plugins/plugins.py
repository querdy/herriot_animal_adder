import re

from lxml import etree
from zeep import Client, Settings, Plugin


class PatchXml(Plugin):
    def egress(self, envelope, http_headers, operation, binding_options):
        request_message = etree.tostring(envelope, encoding="unicode")
        # Check whether envelope contains incorrect XML:
        if "<soap-env:Body>" in request_message:
            request_message = re.sub(r"ns0", "apldef", request_message)
            parser = etree.XMLParser()
            new_envelope = etree.XML(request_message, parser=parser)
            return new_envelope, http_headers
        # If no patching required, return unmodified envelope:
        else:
            return envelope, http_headers
