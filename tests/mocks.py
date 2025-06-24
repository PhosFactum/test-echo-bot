from unittest.mock import MagicMock
from telegram import Update, Message, User
from telegram.ext import CallbackContext

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
