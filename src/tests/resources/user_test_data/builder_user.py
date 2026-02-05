from models.user import User
from tests.resources.user_test_data.mother_object_user import MotherUser
from uuid import UUID

class BuilderUser:

    def __init__(self, base_user=None):
        if base_user is None:
            base_user = MotherUser.default_user()

        self.id = base_user.id
        self.nickname = base_user.nickname
        self.fio = base_user.fio
        self.email = base_user.email
        self.phone_number = base_user.phone_number
        self.password = base_user.password

    def with_id(self, id_number: int):
        self.id = UUID(int=id_number)
        return self

    def with_nickname(self, nickname: str):
        self.nickname = nickname
        return self

    def with_fio(self, fio: str):
        self.fio = fio
        return self

    def with_email(self, email: str):
        self.email = email
        return self

    def with_password(self, password: str):
        self.password = password
        return self



    def build(self):
        """Создает объект Product с текущими настройками"""
        return User(
            id=self.id,
            nickname=self.nickname,
            fio=self.fio,
            email=self.email,
            phone_number=self.phone_number,
            password=self.password
        )


