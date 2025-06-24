import pytest
from main import start, echo, addtime, progression, squares, wait, durations
from tests.mocks import make_update, make_context

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

@pytest.mark.asyncio
async def test_addtime_and_progression():
    durations.clear()

    upd = make_update("/addtime")
    ctx = make_context([])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Использование: /addtime <секунды>")

    upd = make_update("/addtime abc")
    ctx = make_context(["abc"])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Нужно число, например: /addtime 42.5")

    upd = make_update("/addtime 10")
    ctx = make_context(["10"])
    await addtime(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Добавлено время: 10.0 сек. Всего замеров: 1")

    upd = make_update("/addtime 20")
    ctx = make_context(["20"])
    await addtime(upd, ctx)

    upd = make_update("/progression")
    ctx = make_context()
    await progression(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Это геометрическая прогрессия.")

@pytest.mark.asyncio
async def test_squares():
    upd = make_update("/squares")
    ctx = make_context([])
    await squares(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Использование: /squares <числа через пробел>")

    upd = make_update("/squares 1 a 3")
    ctx = make_context(["1", "a", "3"])
    await squares(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Все аргументы должны быть числами.")

    upd = make_update("/squares 2 3 4")
    ctx = make_context(["2", "3", "4"])
    await squares(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Квадраты чисел: 4.00 9.00 16.00")

@pytest.mark.asyncio
async def test_wait(monkeypatch):
    called = {"slept": False}
    
    def fake_sleep(seconds):
        called["slept"] = True
        assert seconds == 2.5

    monkeypatch.setattr("time.sleep", fake_sleep)

    upd = make_update("/wait")
    ctx = make_context([])
    await wait(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Использование: /wait <секунды>")

    upd = make_update("/wait abc")
    ctx = make_context(["abc"])
    await wait(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Нужно число, например: /wait 2.5")

    upd = make_update("/wait 2.5")
    ctx = make_context(["2.5"])
    await wait(upd, ctx)
    upd.message.reply_text.assert_called_once_with("Ожидание 2.5 сек завершено.")
    assert called["slept"]

