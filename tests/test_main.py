# tests/test_main.py
import os
import pytest
from telegram import Update
from telegram.ext import ContextTypes
from main import start, echo

class DummyMessage:
    def __init__(self, text):
        self.text = text
        self.replies = []

    async def reply_text(self, txt):
        self.replies.append(txt)

class DummyUpdate:
    def __init__(self, text):
        self.message = DummyMessage(text)

class DummyContext(ContextTypes.DEFAULT_TYPE):
    pass

@pytest.mark.asyncio
async def test_start():
    upd = DummyUpdate("/start")
    ctx = DummyContext()
    await start(upd, ctx)
    assert "Echo-бот" in upd.message.replies[0]

@pytest.mark.asyncio
async def test_echo():
    text = "hello CI/CD"
    upd = DummyUpdate(text)
    ctx = DummyContext()
    await echo(upd, ctx)
    assert upd.message.replies == [text]

