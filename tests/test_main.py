import pytest
from main import start, echo
from tests.mocks import make_update, make_context

@pytest.mark.asyncio
async def test_start():
    update = make_update("/start")
    context = make_context()
    await start(update, context)
    update.message.reply_text.assert_called_once_with(
        "Привет! Я — Echo-бот. Пришли что угодно, и я повторю."
    )

@pytest.mark.asyncio
async def test_echo():
    text = "hello CI/CD"
    update = make_update(text)
    context = make_context()
    await echo(update, context)
    update.message.reply_text.assert_called_once_with(text)
