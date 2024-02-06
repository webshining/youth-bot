from aiogram.types import BotCommand, BotCommandScopeDefault

from loader import _, bot, i18n


def get_default_commands(lang: str = 'en'):
    commands = [
        BotCommand(command='/start', description=_('start chat', locale=lang)),
        BotCommand(command='/need', description=_('write a need', locale=lang)),
        BotCommand(command='/search', description=_('search song', locale=lang)),
        BotCommand(command='/groups', description=_('get groups', locale=lang)),
        BotCommand(command='/settings', description=_('change settings', locale=lang)),
        BotCommand(command='/cancel', description=_('cancel', locale=lang)),
    ]

    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
    for lang in i18n.available_locales:
        await bot.set_my_commands(get_default_commands(lang), scope=BotCommandScopeDefault(), language_code=lang)
