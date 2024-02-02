import asyncio
import html
import re

from pydantic import BaseModel, model_validator, Field
from requests_html import AsyncHTMLSession

URL = 'https://holychords.pro'


class Song(BaseModel):
    id: int
    name: str
    artist: str
    file: str or None = Field(None)
    text: str or None = Field(None)

    def get_text(self, chords: bool = False) -> str | None:
        if not self.text: return None
        if not chords:
            remove_chords = re.compile(
                r'([|\s]*[A-H][b\#]?(2|5|6|7|9|11|13|\+|\+2|\+4|\+5|\+6|\+7|\+9|\+11|\+13|6\/9|7\-5|7\-9|7\#5|\#5|7\#9|\#9|7\+3|7\+5|7\+9|7b5|7b9|7sus2|7sus4|sus4|add2|add4|add6|add9|aug|dim|dim7|m\/maj7|m6|m7|m7b5|m9|m11|m13|maj|maj7|maj9|maj11|maj13|mb5|m|sus|sus2|sus4|m7add11|add11|b5|-5|4)*[|\s]*)')
            text = '\n'.join([i for i in remove_chords.sub('\n', self.text).split('\n') if i.strip()])
        else:
            text = self.text
        return html.unescape(text)

    @model_validator(mode="before")
    @classmethod
    def isp_name(cls, data: dict) -> str:
        data["file"] = f'{URL}{data["file"]}' if data["file"] else ''
        data["artist"] = data["artist"]["isp_name"]
        return data


async def get_songs(search_name: str) -> list[Song]:
    session = AsyncHTMLSession(loop=asyncio.get_event_loop())
    search_name = '+'.join(search_name.split(' '))
    r = await session.get(f'{URL}/search?name={search_name}', headers={"X-Requested-With": "XMLHttpRequest"})
    return [Song(**i) for i in r.json()["musics"]["data"]]
