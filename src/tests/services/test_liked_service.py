import unittest
from unittest.mock import AsyncMock
import uuid

from models.liked import Liked
from services.liked_service import LikedService


class TestLikedService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repo = AsyncMock()
        self.service = LikedService(self.mock_repo)

        # Создаем тестовые UUID
        self.test_uuid1 = uuid.uuid4()
        self.test_uuid2 = uuid.uuid4()
        self.test_uuid3 = uuid.uuid4()

        self.fake_like = Liked(id=self.test_uuid1, id_customer=self.test_uuid2, id_advert=self.test_uuid3)

    async def test_add_like(self):
        self.mock_repo.add_to_liked.return_value = self.fake_like
        result = await self.service.add_to_liked(self.test_uuid2, self.test_uuid3)
        self.assertEqual(result.id_advert, self.test_uuid3)

    async def test_remove_like(self):
        self.mock_repo.remove_from_liked.return_value = True
        ok = await self.service.remove_from_liked(self.test_uuid2, self.test_uuid3)
        self.assertTrue(ok)

    async def test_get_likes_for_user(self):
        self.mock_repo.get_liked_by_user.return_value = [self.fake_like]
        likes = await self.service.get_liked_by_user(self.test_uuid2)
        self.assertEqual(len(likes), 1)

    async def test_is_liked(self):
        self.mock_repo.is_liked.return_value = True
        self.assertTrue(await self.service.is_liked(self.test_uuid2, self.test_uuid3))
