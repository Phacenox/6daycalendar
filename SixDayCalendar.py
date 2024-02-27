from PIL import ImageDraw
import datetime

import DateBox
from CalendarStyle import CalendarStyle

# makes a rect smaller on all sides, so borders do not bleed into other modules
def pad_rects(rects, padding):
    rects[0] = (rects[0][0] + padding, rects[0][1] + padding)
    rects[1] = (rects[1][0] - padding, rects[1][1] - padding)
    return rects

# draws the title for the month. input is 6day month.
def draw_title(draw: ImageDraw, rects, month: str, calendarStyle: CalendarStyle):
    rects = pad_rects(rects, calendarStyle.stroke_width/2)
    DateBox.draw_shading(rects, draw, (0,0), calendarStyle) #grey shading
    DateBox.draw_border(rects, draw, calendarStyle)
    draw.text(DateBox.base(rects, calendarStyle), month, fill=(0,0,0), anchor="ms", font= calendarStyle.font)

# draws the days of the 6day week in the given rect.
# newday is the extra day at the end of 31 day months.
WEEKDAY_NAMES = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "NEW"]
def draw_weekdays(draw: ImageDraw, rects, calendarStyle: CalendarStyle):
    rects = pad_rects(rects, calendarStyle.stroke_width/2)
    DateBox.draw_border(rects, draw, calendarStyle)
    DateBox.draw_shading(rects, draw, (1,0), calendarStyle) #white shading
    box_width = (rects[1][0] - rects[0][0]) / 7
    for col in range(0, 7):
        weekday_rect = [(rects[0][0] + box_width * col, rects[0][1]), (rects[0][0] + box_width * (col+1), rects[1][1])]
        draw.text(DateBox.base(weekday_rect, calendarStyle), WEEKDAY_NAMES[col], fill=(0,0,0), anchor="ms", font= calendarStyle.small_font)

# yields the column and row for each date in the calendar. overflows max_columns on the last row.
# consider max_columns to be the number of days in a week, excluding extra days at the end of the month.
def date_index_generator(days, max_columns, num_rows):
    col = 0
    row = 0
    for i in range(0, days):
        yield (col, row), i
        col += 1
        if col >= max_columns and row < num_rows - 1:
            col = 0
            row += 1

# draws date boxes in a 7x5 grid. only the first 6 columns are used for the first 30 days
# for months with 31 days, the 7th column is used on the last row.
def draw_dates(draw: ImageDraw, rects, start_date: datetime, days_in_month: int, calendarStyle: CalendarStyle):
    rects = pad_rects(rects, calendarStyle.stroke_width/2)
    box_width = (rects[1][0] - rects[0][0]) / 6
    box_height = (rects[1][1] - rects[0][1]) / 5
    for (col, row), day in date_index_generator(days_in_month, 6, 5):
        if(day+1 == 31):
            DateBox.draw_double_capstone_datebox(box_rect, draw, (col - 1, row), day+1, start_date + datetime.timedelta(days=day), calendarStyle)
            return
        box_rect = [(rects[0][0] + box_width * col, rects[0][1] + box_height * row), (rects[0][0] + box_width * (col+1), rects[0][1] + box_height * (row+1))]
        DateBox.draw_datebox(box_rect, draw, (col, row), day+1, start_date + datetime.timedelta(days=day), calendarStyle)

def draw_calendar_month(draw: ImageDraw, rects, date: datetime, days_in_month: int, month_string: str, calendarStyle: CalendarStyle):
    draw_title(draw, [rects[0], (rects[1][0], calendarStyle.title_height)], month_string, calendarStyle)
    draw_weekdays(draw, [(0, calendarStyle.title_height - calendarStyle.stroke_width), (rects[1][0], calendarStyle.title_height + calendarStyle.weekdays_label_height)], calendarStyle)
    draw_dates(draw, [(0, calendarStyle.title_height + calendarStyle.weekdays_label_height - calendarStyle.stroke_width), rects[1]], date, days_in_month, calendarStyle)
    rects = pad_rects(rects, calendarStyle.stroke_width/2)
    DateBox.draw_border(rects, draw, calendarStyle)