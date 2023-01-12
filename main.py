from PIL import Image, ImageDraw, ImageFont
import sys
import datetime

import SixDayCalendar
from CalendarStyle import CalendarStyle

# defaults
YEAR = 2023
IMG_WIDTH = 1520
IMG_HEIGHT = 1080
STROKE_WIDTH = 5
FONT_SIZE = 50

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if i == 1:
            YEAR = int(arg)
        if i == 2:
            IMG_WIDTH = int(arg)
        if i == 3:
            IMG_HEIGHT = int(arg)
        if i == 4:
            STROKE_WIDTH = int(arg)
        if i == 5:
            FONT_SIZE = int(arg)


def is_leap_year(date: datetime):
    if date.year % 400 == 0:
        return True
    if date.year % 100 == 0:
        return False
    if date.year % 4 == 0:
        return True
    return False

def month_name(month: int):
    month_as_datetime = datetime.datetime(1000, month, 1)
    return month_as_datetime.strftime("%B").upper()

font = ImageFont.truetype("font/coolvetica rg.otf", FONT_SIZE)
half_font = ImageFont.truetype("font/Sansation_Italic.ttf", int(FONT_SIZE/2))
calendarStyle = CalendarStyle(font, half_font, STROKE_WIDTH, FONT_SIZE, FONT_SIZE * 1.2, int(FONT_SIZE/2) * 1.5)

with Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT)) as im:
    draw = ImageDraw.Draw(im)
    date = datetime.datetime(YEAR, 1, 1)
    for month in range(1, 13):
        draw.rectangle((0,0) + (IMG_WIDTH, IMG_HEIGHT), fill=(255,255,255)) # clear canvas
        month_str = month_name(month)
        days_in_month = 31 if month % 2 == 0 else 30
        if month == 2 and not is_leap_year(date): # FEB is only 31 days when it's a leap year
            days_in_month = 30

        SixDayCalendar.draw_calendar_month(draw, [(0,0), (IMG_WIDTH, IMG_HEIGHT)], date, days_in_month, month_str, calendarStyle)

        date = date + datetime.timedelta(days=days_in_month)
        im.save("out/(" + str(month) + ") " + month_str + " " + str(YEAR) + ".png", "PNG")
