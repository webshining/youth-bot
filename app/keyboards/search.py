from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from app.api import Song
from loader import _


def get_songs_markup(data: str, songs: list[Song]):
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text=f"{i + 1}", callback_data=f'{data}_{s.id}') for i, s in enumerate(songs)
    ]
    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup()


def get_song_markup(data: str, id: int, chords: bool = True):
    markup = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text=_("⬅️ Back"), callback_data=f'{data}_back'),
        InlineKeyboardButton(text=_("Chords: On") if not chords else _("Chords: Off"),
                             callback_data=f'{data}_chords_{chords}_{id}'),
        InlineKeyboardButton(text=_("Music"), callback_data=f'{data}_music_{id}', ),
    ]
    markup.add(*buttons)
    markup.adjust(2)

    return markup.as_markup()
