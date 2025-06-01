from pydantic import BaseModel


class ThemeUpdate(BaseModel):
    theme: int

class ColorSetting(BaseModel):
    red_bot: int
    red_top: int
    yellow_bot: int
    yellow_top: int
    green_bot: int
    green_top: int