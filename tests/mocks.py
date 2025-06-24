from unittest.mock import MagicMock
from telegram import Update, Message, User
from telegram.ext import CallbackContext

def make_update(text: str) -> Update:
    update = MagicMock(spec=Update)
    message = MagicMock(spec=Message)
    message.text = text
    update.message = message
    update.effective_user = make_user()
    return update

def make_user() -> User:
    user = MagicMock(spec=User)
    user.id = 123456
    user.first_name = "Test"
    user.is_bot = False
    return user

def make_context(args=None) -> CallbackContext:
    context = MagicMock(spec=CallbackContext)
    context.args = args or []
    context.bot = MagicMock()
    return context

