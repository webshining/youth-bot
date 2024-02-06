from aiogram.types import BotCommand, BotCommandScopeChat

from loader import bot, i18n, _
from .default import get_default_commands


def get_admins_commands(lang: str = 'en'):
    commands = get_default_commands(lang)
    commands.extend([
        BotCommand(command="/needs", description=_("get needs [admin]", locale=lang)),
        BotCommand(command="/needs_clear", description=_("clear needs [admin]", locale=lang))
    ])
    return commands


async def set_admins_commands(id: int):
    await bot.set_my_commands(get_admins_commands(), scope=BotCommandScopeChat(chat_id=id))
    for lang in i18n.available_locales:
        await bot.set_my_commands(get_admins_commands(lang), scope=BotCommandScopeChat(chat_id=id), language_code=lang)
