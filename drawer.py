from PIL import Image, ImageDraw


class Image:
    def __init__(self, img_size, background_color):
        self.image = Image.new("RGBA", img_size, background_color)
        self.draw = ImageDraw.Draw(self.image)

    def draw_line(self, begin, end, line_thickness, line_color):
        self.draw.line(begin + end, line_color, line_thickness)

    def draw_line_strip(self, points, line_thickness, line_color):
        pass

    def draw_rectangle(self, begin, size, border_thickness, border_color, rectangle_color):
        self.draw.rectangle(begin + (begin[0] + size[0], begin[1] + size[1]), rectangle_color)

    def draw_text(self, text, begin, size, font, text_color):
        self.draw.text(begin + (begin[0] + size[0], begin[1] + size[1]), text, text_color, font)

    def save_png(self, file_name):
        # del self.draw
        self.image.save(file_name, 'PNG')
