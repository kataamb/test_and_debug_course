# tests/test_minimal.py
import pytest
import asyncio

@pytest.mark.asyncio
async def test_minimal():
    """Самый простой тест без зависимостей"""
    print(f"✅ Event loop: {asyncio.get_event_loop()}")
    
    # Просто проверяем, что asyncio работает
    await asyncio.sleep(0.01)
    assert True