from PIL import ImageFont

class CalendarStyle:
    stroke_width = 5
    font_size = 60
    font: ImageFont
    small_font: ImageFont
    title_height = 100
    weekdays_label_height = 40

    def __init__(self, font, small_font, stroke_width = 5, font_size = 60, title_height = 100, days_height = 40) -> None:
        self.font = font
        self.small_font = small_font
        self.stroke_width = stroke_width
        self.font_size = font_size
        self.title_height = title_height
        self.weekdays_label_height = days_height
        