from pwdlib import PasswordHash as PWDPasswordHash


class PasswordHash:
    def __init__(self):
        self.__context = PWDPasswordHash.recommended()

    def verify(self, password: str, hashed_password: str):
        return self.__context.verify(password, hashed_password)

    def hash(self, password: str):
        return self.__context.hash(password)
