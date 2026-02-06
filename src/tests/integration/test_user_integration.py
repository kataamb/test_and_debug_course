# tests/integration/test_user_integration.py
"""Интеграционные тесты для UserService с реальной SQLite БД"""
import pytest
from uuid import UUID, uuid4
from service_locator import ServiceLocator
from tests.resources.user_test_data.mother_object_user import MotherUser
from tests.resources.user_test_data.builder_user import BuilderUser
from sqlalchemy import text

from random import randint

class TestUserServiceIntegration:
    """Интеграционные тесты для UserService с реальной SQLite"""

    @pytest.mark.asyncio
    async def test_find_by_email_integration(self, integration_service_locator, integration_db_session):
        """Интеграционный тест поиска пользователя по email"""
        # Arrange - создаем пользователя с УНИКАЛЬНЫМ email
        unique_email = f"test_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()  # Используем uuid4() вместо UUID(int=...)

        await integration_db_session.execute(
            text("""
                INSERT INTO profiles (id, nickname, fio, email, phone_number, password)
                VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
            """),
            {
                "id": str(user_id),
                "nickname": "testuser",
                "fio": "Test User",
                "email": unique_email,
                "phone_number": "+79991112233",
                "password": "password123"
            }
        )
        await integration_db_session.commit()

        # Act
        user_repo = integration_service_locator.repositories.users
        result = await user_repo.find_by_email(unique_email)

        # Assert
        assert result is not None
        assert result.email == unique_email
        assert result.id == user_id

    @pytest.mark.asyncio
    async def test_find_by_email_not_found_integration(self, integration_service_locator):
        """Интеграционный тест поиска несуществующего пользователя по email"""
        # Arrange
        non_existent_email = f"nonexistent_{uuid4().hex[:8]}@example.com"

        # Act
        user_repo = integration_service_locator.repositories.users
        result = await user_repo.find_by_email(non_existent_email)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_create_user_with_unique_email_integration(self, integration_service_locator):
        """Интеграционный тест создания пользователя с уникальным email"""
        # Arrange
        user_repo = integration_service_locator.repositories.users

        # Создаем первого пользователя с уникальным email и UUID
        user1 = MotherUser.default_user()
        user1.email = f"user1_{uuid4().hex[:8]}@example.com"
        user1.id = uuid4()  # Генерируем UUID

        # Создаем второго пользователя с другим уникальным email
        builder = BuilderUser(MotherUser.default_user())
        user2 = builder.with_id(3)  # Генерируем UUID
        user2.email = f"user2_{uuid4().hex[:8]}@example.com"

        # Act - создаем первого пользователя
        result1 = await user_repo.create(user1)

        # Assert
        assert result1 is not None
        assert result1.email == user1.email
        assert result1.id == user1.id

        # Act - создаем второго пользователя с другим email
        result2 = await user_repo.create(user2)

        # Assert
        assert result2 is not None
        assert result2.email == user2.email
        assert result2.id == user2.id

        # Проверяем что оба пользователя в БД
        found1 = await user_repo.find_by_email(user1.email)
        found2 = await user_repo.find_by_email(user2.email)
        assert found1 is not None
        assert found2 is not None

    @pytest.mark.asyncio
    async def test_auth_service_login_integration(self, integration_service_locator, integration_db_session):
        """Интеграционный тест аутентификации пользователя"""
        # Arrange - создаем пользователя напрямую в БД
        unique_email = f"login_test_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()

        await integration_db_session.execute(
            text("""
                INSERT INTO profiles (id, nickname, fio, email, phone_number, password)
                VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
            """),
            {
                "id": str(user_id),
                "nickname": "logintest",
                "fio": "Login Test User",
                "email": unique_email,
                "phone_number": "+79992223344",
                "password": "testpassword123"
            }
        )
        await integration_db_session.commit()

        # Act - используем правильные методы
        auth_service = integration_service_locator.services.auth
        result = await auth_service.login(integration_db_session, unique_email, "testpassword123")

        # Assert - проверяем что вернулся JWT токен
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0  # Токен должен быть не пустой строкой

        # Act - неправильный пароль
        with pytest.raises(ValueError, match="Invalid credentials"):
            await auth_service.login(integration_db_session, unique_email, "wrong_password")

    @pytest.mark.asyncio
    async def test_auth_service_register_integration(self, integration_service_locator, integration_db_session):
        """Интеграционный тест регистрации пользователя"""
        # Arrange
        auth_service = integration_service_locator.services.auth

        unique_email = f"register_test_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()  # Генерируем UUID заранее
        user_data = {
            "id": str(user_id),  # ДОБАВЛЯЕМ ID в данные
            "nickname": "registeruser",
            "fio": "Register Test User",
            "email": unique_email,
            "phone_number": "+79993334455",
            "password": "register_password123",
            "repeat_password": "register_password123"
        }

        # Act - регистрируем пользователя
        registered_user = await auth_service.register(integration_db_session, user_data)

        # Assert - проверяем регистрацию
        assert registered_user is not None
        assert registered_user.email == unique_email
        assert registered_user.nickname == "registeruser"
        assert registered_user.id == user_id  # Проверяем что ID сохранился

        # Проверяем что пользователь действительно создан в БД
        user_repo = integration_service_locator.repositories.users
        found = await user_repo.find_by_email(unique_email)
        assert found is not None
        assert found.email == unique_email
        assert found.id == user_id

    @pytest.mark.asyncio
    async def test_auth_service_register_duplicate_email(self, integration_service_locator, integration_db_session):
        """Тест ошибки при регистрации с существующим email"""
        # Arrange
        auth_service = integration_service_locator.services.auth

        # Создаем пользователя напрямую
        existing_email = f"existing_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()

        await integration_db_session.execute(
            text("""
                INSERT INTO profiles (id, nickname, fio, email, phone_number, password)
                VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
            """),
            {
                "id": str(user_id),
                "nickname": "existinguser",
                "fio": "Existing User",
                "email": existing_email,
                "phone_number": "+79994445566",
                "password": "password123"
            }
        )
        await integration_db_session.commit()

        # Пытаемся зарегистрировать с тем же email
        user_data = {
            "id": str(uuid4()),  # Новый ID
            "nickname": "newuser",
            "fio": "New User",
            "email": existing_email,  # Тот же email!
            "phone_number": "+79995556677",
            "password": "newpassword123",
            "repeat_password": "newpassword123"
        }

        # Act & Assert - должно выбросить исключение
        with pytest.raises(ValueError, match="User already exists"):
            await auth_service.register(integration_db_session, user_data)

    @pytest.mark.asyncio
    async def test_auth_service_register_password_mismatch(self, integration_service_locator, integration_db_session):
        """Тест ошибки при несовпадении паролей при регистрации"""
        # Arrange
        auth_service = integration_service_locator.services.auth

        unique_email = f"password_mismatch_{uuid4().hex[:8]}@example.com"
        user_data = {
            "id": str(uuid4()),  # Генерируем ID
            "nickname": "passworduser",
            "fio": "Password Test User",
            "email": unique_email,
            "phone_number": "+79996667788",
            "password": "password123",
            "repeat_password": "different_password"  # Не совпадает!
        }

        # Act & Assert - должно выбросить исключение
        with pytest.raises(ValueError, match="Passwords didn't matched"):
            await auth_service.register(integration_db_session, user_data)

    @pytest.mark.asyncio
    async def test_create_and_find_user_integration(self, integration_service_locator):
        """Интеграционный тест создания и поиска пользователя"""
        # Arrange
        user_repo = integration_service_locator.repositories.users

        # Создаем уникального пользователя с UUID
        unique_email = f"create_find_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()

        # Используем MotherUser и BuilderUser как требуется
        base_user = MotherUser.default_user()
        builder = BuilderUser(base_user)
        user = builder.with_id(3)  # Устанавливаем UUID
        user.email = unique_email
        user.nickname = "createfinduser"

        # Act - создаем пользователя
        created = await user_repo.create(user)

        # Assert
        assert created is not None
        assert created.email == unique_email
        assert created.id == user_id

        # Act - ищем созданного пользователя
        found = await user_repo.find_by_email(unique_email)

        # Assert
        assert found is not None
        assert found.id == user_id
        assert found.email == unique_email
        assert found.nickname == "createfinduser"

    @pytest.mark.asyncio
    async def test_user_repository_create_error_on_duplicate_email(self, integration_service_locator):
        """Тест ошибки при создании пользователя с дублирующимся email"""
        # Arrange
        user_repo = integration_service_locator.repositories.users

        # Создаем первого пользователя
        email = f"duplicate_{uuid4().hex[:8]}@example.com"
        user1_id = uuid4()

        base_user = MotherUser.default_user()
        builder = BuilderUser(base_user)
        user1 = builder.with_id(3)
        user1.email = email

        await user_repo.create(user1)

        # Пытаемся создать второго пользователя с тем же email
        user2_id = uuid4()
        user2 = builder.with_id(4)
        user2.email = email  # Тот же email!

        # Act & Assert - должно выбросить исключение
        with pytest.raises(Exception) as exc_info:
            await user_repo.create(user2)

        # Проверяем что это ошибка уникальности
        assert "UNIQUE" in str(exc_info.value) or "duplicate" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_user_fields_persistence_integration(self, integration_service_locator):
        """Тест сохранения всех полей пользователя"""
        # Arrange
        user_repo = integration_service_locator.repositories.users

        # Создаем пользователя со всеми полями
        unique_email = f"fulluser_{uuid4().hex[:8]}@example.com"
        user_id = uuid4()

        base_user = MotherUser.default_user()
        builder = BuilderUser(base_user)
        user = builder.with_id(3)
        user.email = unique_email
        user.nickname = "fullusertest"
        user.fio = "Иванов Иван Иванович"
        user.phone_number = "+79998887766"
        user.password = "complex_password_123!"

        # Act
        created = await user_repo.create(user)

        # Assert - проверяем создание
        assert created is not None
        assert created.email == unique_email
        assert created.nickname == "fullusertest"
        assert created.fio == "Иванов Иван Иванович"
        assert created.phone_number == "+79998887766"
        assert created.id == user_id

        # Act - ищем пользователя
        found = await user_repo.find_by_email(unique_email)

        # Assert - проверяем все поля
        assert found is not None
        assert found.id == user_id
        assert found.email == unique_email
        assert found.nickname == "fullusertest"
        assert found.fio == "Иванов Иван Иванович"
        assert found.phone_number == "+79998887766"