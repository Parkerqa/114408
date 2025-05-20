from pydantic import BaseModel


class ThemeUpdate(BaseModel):
    theme: int

class ColorSetting(BaseModel):
    red_but: int
    red_top: int
    yellow_but: int
    yellow_top: int
    green_but: int
    green_top: int