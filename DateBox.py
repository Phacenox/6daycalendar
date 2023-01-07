from PIL import ImageDraw, ImageFont
import datetime
import math



STROKE_WIDTH = 5
FONT_SIZE = 60

def midpoint(rects) -> tuple:
    return (rects[0][0] / 2 + rects[1][0] / 2, rects[0][1] / 2 + rects[1][1] / 2)
def base(rects) -> tuple:
    return (rects[0][0] / 2 + rects[1][0] / 2, rects[1][1] - STROKE_WIDTH - FONT_SIZE / 10)

# Adjusts a line to be STROKE_WIDTH longer, to fix square border corners.
# Assumes a straight vertical or horizontal line.
def adjust_line(points):
    direction = 0 if points[0][0] != points[1][0] else 1 #determines if its vertical or horizontal
    sign = 1 if points[0][direction] < points[1][direction] else -1
    ret = [0,0,0,0] #need to convert to the other format ImageDraw uses since tuples are immutable.
    ret[direction] = points[0][direction] - math.floor(STROKE_WIDTH/2) * sign
    ret[2+direction] = points[1][direction] + math.floor(STROKE_WIDTH/2) * sign
    ret[(1-direction)] = points[0][1-direction]
    ret[2+(1-direction)] = points[1][1-direction]
    return ret


def draw_border(rects, draw: ImageDraw):
    other_corners = [(rects[0][0], rects[1][1]), (rects[1][0], rects[0][1])]
    for i in rects:
        for j in other_corners:
            draw.line(adjust_line([i, j]), fill=(0,0,0), width= STROKE_WIDTH)

def draw_shading(rects, draw: ImageDraw, day_grid_position: tuple, datetime: datetime = None):
    if day_grid_position[0] == 0 or day_grid_position[0] >= 5: #highlight 6day weekends
        draw.rectangle(rects, fill=(200,200,200))
    if(datetime != None and datetime.weekday() == 0): #highlight 7day mondays
        draw.rectangle([(rects[0][0], rects[1][1] - FONT_SIZE/1.4), (rects[1])], fill=(50,200,50))

def draw_labels(rects, draw:ImageDraw, day: int, datetime: datetime, font: ImageFont, half_font: ImageFont):
    draw.text(midpoint(rects), str(day), fill=(0,0,0), anchor="mm", font = font)
    draw.text(base(rects), datetime.strftime("%a, %b %d"), fill=(70,70,70), anchor="ms", font= half_font)

def draw_datebox(rects, draw: ImageDraw, day_grid_position: tuple, day: int, datetime: datetime, font: ImageFont, half_font: ImageFont):
    draw_shading(rects, draw, day_grid_position, datetime)
    draw_border(rects, draw)
    draw_labels(rects, draw, day, datetime, font, half_font)