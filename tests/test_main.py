import pytest
import time
from unittest.mock import MagicMock
from telegram import Update, Message, User
from telegram.ext import CallbackContext
from main import start, echo, addtime, progression, squares, wait, durations

# Упрощённые моки прямо в тестовом файле
def make_update(text: str) -> Update:
    update = MagicMock(spec=Update)
    message = MagicMock(spec=Message)
    message.text = text
    update.message = message
    return update

def make_context(args=None) -> CallbackContext:
    context = MagicMock(spec=CallbackContext)
    context.args = args or []
    return context

# Быстрые тесты (оставлены для примера)
@pytest.mark.asyncio
async def test_start():
    update = make_update("/start")
    ctx = make_context()
    await start(update, ctx)
    update.message.reply_text.assert_called_once_with(
        "Привет! Я — Echo-бот. Пришли что угодно, и я повторю."
    )

@pytest.mark.asyncio
async def test_echo():
    text = "hello CI/CD"
    update = make_update(text)
    ctx = make_context()
    await echo(update, ctx)
    update.message.reply_text.assert_called_once_with(text)

import pytest
import time
from unittest.mock import MagicMock
from telegram import Update, Message, User
from telegram.ext import CallbackContext
from main import start, echo, addtime, progression, squares, wait, durations

# Упрощённые моки прямо в тестовом файле
def make_update(text: str) -> Update:
    update = MagicMock(spec=Update)
    message = MagicMock(spec=Message)
    message.text = text
    update.message = message
    return update

def make_context(args=None) -> CallbackContext:
    context = MagicMock(spec=CallbackContext)
    context.args = args or []
    return context

# Быстрые тесты (оставлены для примера)
@pytest.mark.asyncio
async def test_start():
    update = make_update("/start")
    ctx = make_context()
    await start(update, ctx)
    update.message.reply_text.assert_called_once_with(
        "Привет! Я — Echo-бот. Пришли что угодно, и я повторю."
    )

@pytest.mark.asyncio
async def test_echo():
    text = "hello CI/CD"
    update = make_update(text)
    ctx = make_context()
    await echo(update, ctx)
    update.message.reply_text.assert_called_once_with(text)

# Медленные тесты (10-15 секунд)
@pytest.mark.asyncio
async def test_long_operations():
    """Тест с реальными длительными операциями"""
    # 1. Долгое вычисление квадратов (2-10000)
    start_time = time.time()
    numbers = list(range(2, 10001))
    args = [str(n) for n in numbers]
    
    update = make_update(f"/squares {' '.join(args)}")
    ctx = make_context(args)
    await squares(update, ctx)
    
    squares_time = time.time() - start_time
    print(f"\nВычисление 9998 квадратов заняло: {squares_time:.2f} сек")
    
    # 2. Реальное ожидание (5 секунд)
    update = make_update("/wait 5")
    ctx = make_context(["5"])
    await wait(update, ctx)
    
    # 3. Ещё одно долгое вычисление (факториалы 1-500)
    def factorial(n):
        result = 1
        for i in range(1, n+1):
            result *= i
        return result
    
    start_time = time.time()
    for n in range(1, 501):
        factorial(n)
    factorial_time = time.time() - start_time
    print(f"Вычисление 500 факториалов заняло: {factorial_time:.2f} сек")
    
    # 4. Ещё одно ожидание (5 секунд)
    update = make_update("/wait 5")
    ctx = make_context(["5"])
    await wait(update, ctx)
    
    # Проверяем что общее время > 10 сек
    total_time = time.time() - start_time
    print(f"Общее время теста: {total_time:.2f} сек")
    assert total_time < 10
