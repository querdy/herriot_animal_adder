import time
import uuid
from datetime import datetime, timedelta, timezone

# pip install pyjwt
import jwt
import machineid
from loguru import logger


class TokenError(Exception): ...


class MachineJWT:
    _salt = ""

    def __init__(self, machine_id: str):
        self._machine_id = machine_id

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                key=self._salt,
                algorithms=("HS256",),
                issuer=self._machine_id,
            )
        except jwt.ExpiredSignatureError:
            raise TokenError("Необходимо получить новый ключ")
        except jwt.InvalidIssuerError:
            raise TokenError("Ключ выдан для другого компьютера")
        except jwt.PyJWTError as err:
            raise TokenError(f"Непредвиденная ошибка анализа ключа [{err}]")


def load_license() -> str:
    _license = ""
    try:
        with open("license", "r") as file:
            _license = file.read()
        return _license
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с лицензионным ключом не обнаружен")
    # finally:
    #     return _license


def save_license(key: str) -> None:
    try:
        with open("license", "w") as file:
            file.write(key)
    except Exception as err:
        logger.warning(f"Непредвиденная ошибка [{err}]")
