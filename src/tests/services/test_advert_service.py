import unittest
from unittest.mock import AsyncMock
import uuid

from models.advert import Advert
from services.advert_service import AdvertService
from abstract_repositories.iadvert_repository import IAdvertRepository


class TestAdvertService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.repo = AsyncMock(spec=IAdvertRepository)
        self.service = AdvertService(self.repo)

        # Создаем тестовые UUID
        self.test_uuid1 = uuid.uuid4()
        self.test_uuid2 = uuid.uuid4()
        self.test_uuid3 = uuid.uuid4()
        self.test_uuid4 = uuid.uuid4()
        self.test_uuid5 = uuid.uuid4()

        self.advert = Advert(
            id=self.test_uuid1,
            content="Контент",
            description="Описание",
            id_category=self.test_uuid2,
            price=1500,
            id_seller=self.test_uuid3,
        )
        self.advert_other = Advert(
            id=self.test_uuid4,
            content="Другой",
            description="Описание 2",
            id_category=self.test_uuid5,
            price=2500,
            id_seller=self.test_uuid3,  # тот же продавец
        )

    async def test_create_advert(self):
        self.repo.create.return_value = self.advert
        created = await self.service.create_advert(self.advert)
        self.assertEqual(created.id, self.test_uuid1)
        self.repo.create.assert_awaited_once_with(self.advert)

    async def test_get_advert_found(self):
        self.repo.get_by_id.return_value = self.advert
        found = await self.service.get_advert(self.test_uuid1)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.test_uuid1)
        self.repo.get_by_id.assert_awaited_once_with(self.test_uuid1)


    async def test_get_all_adverts(self):
        self.repo.get_all_adverts.return_value = [self.advert, self.advert_other]
        items = await self.service.get_all_adverts()
        self.assertEqual(len(items), 2)
        self.repo.get_all_adverts.assert_awaited_once()

    async def test_get_advert_by_user(self):
        self.repo.get_advert_by_user.return_value = [self.advert, self.advert_other]
        items = await self.service.get_advert_by_user(self.test_uuid3)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].id_seller, self.test_uuid3)
        self.assertEqual(items[1].id_seller, self.test_uuid3)
        self.repo.get_advert_by_user.assert_awaited_once_with(self.test_uuid3)

    async def test_get_adverts_by_category(self):
        self.repo.get_adverts_by_category.return_value = [self.advert]
        items = await self.service.get_adverts_by_category(self.test_uuid2)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id_category, self.test_uuid2)
        self.repo.get_adverts_by_category.assert_awaited_once_with(self.test_uuid2)

    async def test_get_adverts_by_key_word(self):
        self.repo.get_adverts_by_key_word.return_value = [self.advert]
        items = await self.service.get_adverts_by_key_word("Контент")
        self.assertEqual(len(items), 1)
        self.assertIn("Контент", items[0].content)
        self.repo.get_adverts_by_key_word.assert_awaited_once_with("Контент")

    async def test_is_created_true(self):
        self.repo.is_created.return_value = True
        self.assertTrue(await self.service.is_created(self.test_uuid3, self.test_uuid1))
        self.repo.is_created.assert_awaited_once_with(self.test_uuid3, self.test_uuid1)



