from zeep import Client


class VetisFactory:
    def __init__(self, client: Client):
        self.client = client

    def __getattr__(self, item):
        return self.client.type_factory(item)
