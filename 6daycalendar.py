from PIL import Image, ImageDraw, ImageFont
import sys
import datetime
import DateBox


YEAR = 2023
IMG_WIDTH = 1920
IMG_HEIGHT = 1080
STROKE_WIDTH = 5
FONT_SIZE = 60

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

# makes a rect smaller on all sides
def pad_rects(rects, padding):
    rects[0] = (rects[0][0] + padding, rects[0][1] + padding)
    rects[1] = (rects[1][0] - padding, rects[1][1] - padding)
    return rects

# draws date boxes in a 7x5 grid. only the first 5 columns are used for the first 30 days
# for months with 31 days, the 6th column is used on the last row.
# datebox automatically marks 6day weekends as gray and 7day mondays with a green stripe.
def draw_dates(draw: ImageDraw, rects, start_date: datetime, days_in_month: int):
    rects = pad_rects(rects, STROKE_WIDTH/2)
    box_width = (rects[1][0] - rects[0][0]) / 7
    box_height = (rects[1][1] - rects[0][1]) / 5
    row = 0
    col = 0
    for i in range(0, days_in_month):
        boxrects = [(rects[0][0] + box_width * col, rects[0][1] + box_height * row), (rects[0][0] + box_width * (col+1), rects[0][1] + box_height * (row+1))]
        DateBox.draw_datebox(boxrects, draw, (col, row), i+1, start_date + datetime.timedelta(days=i), font, half_font)
        col += 1
        if row < 4 and col >= 6:
            col = 0
            row += 1

# draws the title for the month. input is 6day month.
def draw_title(draw: ImageDraw, rects, month: str, font: ImageFont):
    rects = pad_rects(rects, STROKE_WIDTH/2)
    DateBox.draw_shading(rects, draw, (0,0)) #grey shading
    DateBox.draw_border(rects, draw)
    draw.text(DateBox.base(rects), month, fill=(0,0,0), anchor="ms", font= font)

# draws the days of the 6day week in the given rect.
# newday is the extra day at the end of 31 day months.
WEEKDAY_NAMES = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "NEW"]
def draw_days(draw: ImageDraw, rects, font: ImageFont):
    rects = pad_rects(rects, STROKE_WIDTH/2)
    DateBox.draw_border(rects, draw)
    DateBox.draw_shading(rects, draw, (1,0)) #white shading
    box_width = (rects[1][0] - rects[0][0]) / 7
    for col in range(0, 7):
        weekday_rect = [(rects[0][0] + box_width * col, rects[0][1]), (rects[0][0] + box_width * (col+1), rects[1][1])]
        draw.text(DateBox.base(weekday_rect), WEEKDAY_NAMES[col], fill=(0,0,0), anchor="ms", font= font)
        pass

def is_leap_year(date: datetime):
    if date.year % 400 == 0:
        return True
    if date.year % 100 == 0:
        return False
    if date.year % 4 == 0:
        return True
    return False

font = ImageFont.truetype("coolvetica rg.otf", FONT_SIZE)
half_font = ImageFont.truetype("Sansation_Italic.ttf", int(FONT_SIZE/2))
with Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT)) as im:
    draw = ImageDraw.Draw(im)
    DateBox.STROKE_WIDTH = STROKE_WIDTH
    DateBox.FONT_SIZE = FONT_SIZE
    title_height = FONT_SIZE * 1.2
    days_height = int(FONT_SIZE/2) * 1.5
    date = datetime.datetime(YEAR, 1, 1)
    for month in range(1, 13):
        draw.rectangle((0,0) + (IMG_WIDTH, IMG_HEIGHT), fill=(255,255,255)) #clear canvas
        month_as_datetime = datetime.datetime(1000, month, 1)
        month_str = month_as_datetime.strftime("%B").upper()
        days_in_month = 31 if month % 2 == 0 else 30
        if month == 2 and not is_leap_year(date): #FEB is only 31 days when it's a leap year
            days_in_month = 30

        draw_title(draw, [(0, 0), (IMG_WIDTH, title_height)], month_str, font)
        draw_days(draw, [(0, title_height - STROKE_WIDTH), (IMG_WIDTH, title_height + days_height)], half_font)
        draw_dates(draw, [(0, title_height + days_height - STROKE_WIDTH), (IMG_WIDTH, IMG_HEIGHT)], date, days_in_month)

        date = date + datetime.timedelta(days=days_in_month)
        im.save("out/(" + str(month) + ") " + month_str + " " + str(YEAR) + ".png", "PNG")
