import unittest
from unittest.mock import AsyncMock
import uuid

from models.advert import Advert
from models.deal import Deal
from services.deal_service import DealsService
from abstract_repositories.ideal_repository import IDealRepository


class TestDealsService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.repo = AsyncMock(spec=IDealRepository)
        self.service = DealsService(self.repo)

        # Создаем тестовые UUID
        self.test_uuid1 = uuid.uuid4()
        self.test_uuid2 = uuid.uuid4()
        self.test_uuid3 = uuid.uuid4()
        self.test_uuid4 = uuid.uuid4()
        self.test_uuid5 = uuid.uuid4()

        self.fake_deal = Deal(id=self.test_uuid1, id_customer=self.test_uuid2, id_advert=self.test_uuid3)
        self.fake_advert = Advert(
            id=self.test_uuid3,
            content="Тестовый контент",
            description="Описание объявления",
            id_category=self.test_uuid4,
            price=1000,
            id_seller=self.test_uuid5,
        )

    async def test_create_deal(self):
        self.repo.create_deal.return_value = self.fake_deal
        result = await self.service.create_deal(self.test_uuid2, self.test_uuid3)
        self.assertEqual(result.id_advert, self.test_uuid3)
        self.repo.create_deal.assert_awaited_once_with(self.test_uuid2, self.test_uuid3)

    async def test_get_deals_by_user(self):
        # Репозиторий возвращает список Advert
        self.repo.get_deals_by_user.return_value = [self.fake_advert]
        adverts = await self.service.get_deals_by_user(self.test_uuid5)
        self.assertEqual(len(adverts), 1)
        self.assertEqual(adverts[0].id, self.test_uuid3)
        self.assertEqual(adverts[0].id_seller, self.test_uuid5)
        self.repo.get_deals_by_user.assert_awaited_once_with(self.test_uuid5)

    async def test_is_in_deals(self):
        self.repo.is_in_deals.return_value = True
        self.assertTrue(await self.service.is_in_deals(self.test_uuid2, self.test_uuid3))
        self.repo.is_in_deals.assert_awaited_once_with(self.test_uuid2, self.test_uuid3)
