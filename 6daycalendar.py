from PIL import Image, ImageDraw, ImageFont
import sys
import datetime


YEAR = 2023
IMG_WIDTH = 1920
IMG_HEIGHT = 1080
STROKE_WIDTH = 5
FONT_SIZE = 60

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if i == 1:
            YEAR = int(arg)
        if i == 1:
            IMG_WIDTH = int(arg)
        if i == 2:
            IMG_HEIGHT = int(arg)
        if i == 3:
            STROKE_WIDTH = int(arg)

def draw_borders(draw: ImageDraw, color):
    pass

def draw_shading(draw: ImageDraw):
    pass

def draw_labels(draw: ImageDraw):#and icons
    pass


class DateBox:
    rect1 = (0,0)
    rect2 = (0,0)
    children = []

    def midpoint(self) -> tuple:
        return (self.rect1[0] / 2 + self.rect2[0] / 2, self.rect1[1] / 2 + self.rect2[1] / 2 - FONT_SIZE/2)
    def base(self) -> tuple:
        return (self.rect1[0] / 2 + self.rect2[0] / 2, self.rect2[1] - FONT_SIZE/2)

    def __init__(self, rect1: tuple, rect2: tuple):
        self.rect1 = rect1
        self.rect2 = rect2
    
    def draw_borders(self, draw: ImageDraw):
        draw.line(self.rect1 + (self.rect1[0], self.rect2[1]), fill=(0,0,0), width = STROKE_WIDTH)
        draw.line(self.rect1 + (self.rect2[0], self.rect1[1]), fill=(0,0,0), width = STROKE_WIDTH)
        draw.line(self.rect2 + (self.rect1[0], self.rect2[1]), fill=(0,0,0), width = STROKE_WIDTH)
        draw.line(self.rect2 + (self.rect2[0], self.rect1[1]), fill=(0,0,0), width = STROKE_WIDTH)

    def draw_shading(self, draw: ImageDraw, day_grid_position: tuple):
        if day_grid_position[0] == 0 or day_grid_position[0] >= 5:
            draw.rectangle([self.rect1, self.rect2],fill=(200,200,200))
    
    def draw_labels(self, draw:ImageDraw, day: int, datetime: datetime, font: ImageFont, half_font: ImageFont):
        draw.text(self.midpoint(), str(day), fill=(0,0,0), anchor="mt", font = font)
        draw.text(self.base(), datetime.strftime("%a, %b %d"), fill=(50,50,50), anchor="ms", font= half_font)
    
def draw_dates(draw: ImageDraw, rect1: tuple, rect2: tuple, start_date: datetime, days_in_month: int):
    box_width = (rect2[0] - rect1[0]) / 7
    box_height = (rect2[1] - rect1[1]) / 5
    row = 0
    col = 0
    for i in range(0, days_in_month):
        db = DateBox( (rect1[0] + box_width * col, rect1[1] + box_height * row), (rect1[0] + box_width * col + box_width, rect1[1] + box_height * row + box_height) )
        db.draw_shading(draw, (col, row))
        db.draw_borders(draw)
        db.draw_labels(draw, i+1, start_date + datetime.timedelta(days=i), font, half_font)
        col += 1
        if row < 4 and col >= 6:
            col = 0
            row += 1


font = ImageFont.truetype("coolvetica rg.otf", FONT_SIZE)
half_font = ImageFont.truetype("Sansation_Italic.ttf", int(FONT_SIZE/2))
with Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT)) as im:
    draw = ImageDraw.Draw(im)
    draw.rectangle((0,0) + (IMG_WIDTH, IMG_HEIGHT), fill=(255,255,255))

    draw_dates(draw, (0,0), (IMG_WIDTH, IMG_HEIGHT), datetime.datetime(2023, 1, 1), 31)

    im.save("calendar.png", "PNG")
