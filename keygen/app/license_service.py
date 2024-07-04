from datetime import datetime, timedelta, timezone

import jwt


class TokenError(Exception):
    ...


class MachineJWT:
    _salt = ""

    def __init__(self, machine_id: str):
        self._machine_id = machine_id

    def encode(self, exp: timedelta, district: list[str], **extra) -> str:
        data = {
            "exp": datetime.now(tz=timezone.utc) + exp,
            "iss": self._machine_id,
            "district": district,
            **extra
        }
        return jwt.encode(
            data,
            self._salt,
        )

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                key=self._salt,
                algorithms=('HS256',),
                issuer=self._machine_id,
            )
        except jwt.ExpiredSignatureError:
            raise TokenError("Необходимо получить новый ключ")
        except jwt.InvalidIssuerError:
            raise TokenError("Ключ выдан для другого компьютера")
        except jwt.PyJWTError as err:
            raise TokenError(f"Непредвиденная ошибка анализа ключа [{err}]")



