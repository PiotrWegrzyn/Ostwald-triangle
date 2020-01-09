from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle


class Annotation(Rectangle):
    def __init__(self, text, pos, *args, **kwargs):
        if kwargs.get("format", None):
            text = self.format(text, kwargs.get("format", None))
        scale = kwargs.get("scale", 1)
        resolution_scaled_size = ((16/3360)*Window.size[0], (32/2100)*Window.size[1])
        size = [len(str(text)) * resolution_scaled_size[0] * scale, resolution_scaled_size[1] * scale]
        offset_x = kwargs.get("offset_x", 0) * Window.size[0]/1650
        offset_y = kwargs.get("offset_y", 0) * Window.size[1]/1050
        pos = (pos[0]-(size[0]/2)+offset_x, pos[1]-(size[1]/2)+offset_y)
        super().__init__(texture=self.get_texture(text), pos=pos, size=size, *args, **kwargs)

    def format(self, text, format):
        if format is "float":
            text = self.format_float(text)
        return text

    @classmethod
    def format_float(cls, annotation):
        if isinstance(annotation, float):
            annotation = cls.limit_to_percision2(annotation)
            annotation = cls.remove_redundant_zeros(annotation)
        return annotation

    @staticmethod
    def remove_redundant_zeros(annotation):
        if annotation % 1 == 0:
            return int(annotation)
        return annotation

    @staticmethod
    def get_texture(text):
        l = CoreLabel()
        l.text = str(text)
        l.refresh()
        return l.texture

    @classmethod
    def limit_to_percision2(cls, fnumber):
        return float("{0:.3f}".format(fnumber))
