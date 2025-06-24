import pytest
from unittest.mock import MagicMock
from telegram import Update, Message, User
from telegram.ext import CallbackContext

from main import start, echo, addtime, progression, durations

# === Мок-фабрики ===
def make_update(text: str) -> Update:
    u = MagicMock(spec=Update)
    m = MagicMock(spec=Message)
    m.text = text
    u.message = m
    u.effective_user = make_user()
    return u

def make_user() -> User:
    u = MagicMock(spec=User)
    u.id = 123456
    u.first_name = "Test"
    u.is_bot = False
    return u

def make_context(args=None) -> CallbackContext:
    ctx = MagicMock(spec=CallbackContext)
    ctx.args = args or []
    ctx.bot = MagicMock()
    return ctx

# === Тесты ===
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
    txt = "hello CI/CD"
    update = make_update(txt)
    ctx = make_context()
    await echo(update, ctx)
    update.message.reply_text.assert_called_once_with(txt)

@pytest.mark.asyncio
async def test_addtime_and_progression():
    durations.clear()

    # 1) без аргументов
    upd = make_update("/addtime")
    ctx = make_context([])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Использование: /addtime <секунды>")

    # 2) неверный формат
    upd = make_update("/addtime abc")
    ctx = make_context(["abc"])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Нужно число, например: /addtime 42.5")

    # 3) правильные добавления
    upd = make_update("/addtime 10")
    ctx = make_context(["10"])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Добавлено время: 10.0 сек. Всего замеров: 1")

    upd = make_update("/addtime 20")
    ctx = make_context(["20"])
    await addtime(upd, ctx)
    # durations == [10.0, 20.0]

    # 4) проверка прогрессии
    upd = make_update("/progression")
    ctx = make_context()
    await progression(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Это геометрическая прогрессия.")

