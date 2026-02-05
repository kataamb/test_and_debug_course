from models.user import User
from uuid import UUID

class MotherUser:
    @staticmethod
    def default_user() -> User:
        return User(
            id=UUID(int=1),
            nickname="nickname1",
            fio = "Petrov Pavel",
            email = "pp1@mail.ru",
            phone_number = "+773",
            password = "123"

        )

    @staticmethod
    def petrov_pavel() -> User:
        return User(
            id=UUID(int=1),
            nickname="nickname1",
            fio="Petrov Pavel",
            email="pp1@mail.ru",
            phone_number="+773",
            password="123"

        )
