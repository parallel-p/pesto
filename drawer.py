import PIL.Image
import PIL.ImageDraw


def RGB(r, g, b):
    return 2 ** 16 * b + 2 ** 8 * g + r


class Image:
    def __init__(self, img_size, background_color):
        self.image = PIL.Image.new("RGB", img_size, background_color)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def draw_line(self, begin, end, line_thickness, line_color):
        self.draw.line(begin + end, line_color, line_thickness)

    def draw_line_strip(self, points, line_thickness, line_color):
        for start_point, end_point in zip(points, points[1:]):
            self.draw_line(start_point, end_point, line_thickness, line_color)

    # begin is a tuple (x0, y0), size is a tuple (size_x, size_y)
    def draw_rectangle(self, begin, size, border_thickness, border_color, rectangle_color):
        self.draw.rectangle(begin + (begin[0] + size[0], begin[1] + size[1]), rectangle_color, border_color)

    def draw_text(self, text, begin, size, font, text_color):
        self.draw.text(begin + (begin[0] + size[0], begin[1] + size[1]), text, text_color)

    def save_png(self, file_name):
        self.image.save(file_name, 'BMP')
