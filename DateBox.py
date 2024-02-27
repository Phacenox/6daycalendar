from PIL import ImageDraw
import datetime
import math
import numpy

from CalendarStyle import CalendarStyle

def midpoint(rects) -> tuple:
    return (rects[0][0] / 2 + rects[1][0] / 2, rects[0][1] / 2 + rects[1][1] / 2)
# returns the base of a rect, slightly upwards to compensate for both border width and font tails.
def base(rects, calendarStyle: CalendarStyle) -> tuple:
    return (rects[0][0] / 2 + rects[1][0] / 2, rects[1][1] - calendarStyle.stroke_width - calendarStyle.font_size / 10)
def top(rects, calendarStyle: CalendarStyle) -> tuple:
    return (rects[0][0] / 2 + rects[1][0] / 2, rects[0][1] + calendarStyle.stroke_width + calendarStyle.font_size / 10)

# Adjusts a line to be STROKE_WIDTH longer, to fix square border corners.
# Assumes a straight vertical or horizontal line.
def adjust_line(points, calendarStyle: CalendarStyle):
    direction = 0 if points[0][0] != points[1][0] else 1 #determines if its vertical or horizontal
    sign = 1 if points[0][direction] < points[1][direction] else -1
    ret = [0,0,0,0] #need to convert to the other format ImageDraw uses since tuples are immutable.
    ret[direction] = points[0][direction] - math.floor(calendarStyle.stroke_width/2) * sign
    ret[2+direction] = points[1][direction] + math.floor(calendarStyle.stroke_width/2) * sign
    ret[(1-direction)] = points[0][1-direction]
    ret[2+(1-direction)] = points[1][1-direction]
    return ret


def draw_border(rects, draw: ImageDraw, calendarStyle: CalendarStyle):
    other_corners = [(rects[0][0], rects[1][1]), (rects[1][0], rects[0][1])]
    for i in rects:
        for j in other_corners:
            draw.line(adjust_line([i, j], calendarStyle), fill=(0,0,0), width= calendarStyle.stroke_width)

def draw_shading(rects, draw: ImageDraw, day_grid_position: tuple, calendarStyle: CalendarStyle, datetime: datetime = None):
    # highlight 6day weekends
    if day_grid_position[0] == 0 or day_grid_position[0] >= 5:
        draw.rectangle(rects, fill=(220,220,220))
    # highlight 7day mondays
    if(datetime != None and datetime.weekday() == 0):
        draw.rectangle([(rects[0][0], rects[1][1] - calendarStyle.font_size/1.4), (rects[1])], fill=(150,255,150))

def draw_labels(rects, draw:ImageDraw, day: int, datetime: datetime, calendarStyle: CalendarStyle):
    # day of 6day month
    draw.text(midpoint(rects), str(day), fill=(0,0,0), anchor="mm", font = calendarStyle.font)
    # full date string of standard date
    draw.text(base(rects, calendarStyle), datetime.strftime("%a, %b %d"), fill=(70,70,70), anchor="ms", font= calendarStyle.small_font)

def draw_datebox(rects, draw: ImageDraw, day_grid_position: tuple, day: int, datetime: datetime, calendarStyle: CalendarStyle):
    draw_shading(rects, draw, day_grid_position, calendarStyle, datetime)
    draw_border(rects, draw, calendarStyle)
    draw_labels(rects, draw, day, datetime, calendarStyle)

#draws a box split diagonally, using styles of the input date and the previous date
def draw_double_capstone_datebox(rects, draw: ImageDraw, day_grid_position: tuple, day: int, date_time: datetime, calendarStyle: CalendarStyle):
    date_time_yesterday = date_time - datetime.timedelta(days=1)
    # highlight 6day weekends
    if day_grid_position[0] == 0 or day_grid_position[0] >= 5:
        draw.rectangle(rects, fill=(220,220,220))
    # highlight 7day mondays
    if(date_time != None and date_time_yesterday.weekday() == 0):
        draw.rectangle([rects[0], (rects[1][0], rects[0][1] + calendarStyle.font_size/1.4)], fill=(150,255,150))
    if(date_time != None and date_time.weekday() == 0):
        draw.rectangle([(rects[0][0], rects[1][1] - calendarStyle.font_size/1.4), (rects[1])], fill=(150,255,150))
    
    draw_border(rects, draw, calendarStyle)
    draw.line([(rects[0][0], rects[1][1] - calendarStyle.font_size/1.4), (rects[1][0], rects[0][1] + calendarStyle.font_size/1.4)], fill=(0,0,0), width= calendarStyle.stroke_width)

    # day of 6day month
    draw.text(numpy.subtract(midpoint(rects), (calendarStyle.font_size* 0.75,calendarStyle.font_size/2)), str(day-1), fill=(0,0,0), anchor="rm", font = calendarStyle.font)
    draw.text(numpy.add(midpoint(rects), (calendarStyle.font_size * 0.75,calendarStyle.font_size/2)), str(day), fill=(0,0,0), anchor="lm", font = calendarStyle.font)
    # full date string of standard date
    draw.text(top(rects, calendarStyle), date_time_yesterday.strftime("%a, %b %d"), fill=(70,70,70), anchor="mt", font= calendarStyle.small_font)
    draw.text(base(rects, calendarStyle), date_time.strftime("%a, %b %d"), fill=(70,70,70), anchor="ms", font= calendarStyle.small_font)