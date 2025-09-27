from pydantic import BaseModel


class ThemeUpdate(BaseModel):
    theme: int


class ColorSetting(BaseModel):
    red_usage_rate: int
    red_remaining_rate: int
    green_usage_rate: int
    green_remaining_rate: int
    yellow_usage_rate: int
    yellow_remaining_rate: int
