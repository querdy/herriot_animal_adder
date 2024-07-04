import requests
from requests import Session
from requests.auth import HTTPBasicAuth


def http_login(enterprise_login: str, enterprise_password: str) -> Session:
    session = Session()
    session.verify = True
    session.auth = HTTPBasicAuth(enterprise_login, enterprise_password)
    return session
