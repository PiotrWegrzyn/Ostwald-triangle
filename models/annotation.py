from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.text import Label as CoreLabel


class Annotation(Rectangle):
    def __init__(self, text, pos, *args, **kwargs):
        if kwargs.get("format", None):
            text = self.format(kwargs["format"], text)
        l = CoreLabel()
        l.text = str(text)
        l.refresh()
        scale = kwargs.get("scale", 1)
        kwargs['texture'] = l.texture
        kwargs['pos'] = pos
        kwargs['size'] = [len(str(text)) * 8 * scale, 15 * scale]
        super().__init__(*args, **kwargs)

    def format(self, kwargs, text):
        if kwargs['format'] is float:
            text = self.format_float(text)
        return text

    @classmethod
    def format_float(cls, annotation):
        if isinstance(annotation, float):
            annotation = cls.remove_trailing_zero(annotation)
        return annotation

    @staticmethod
    def remove_trailing_zero(annotation):
        if annotation % 1 == 0:
            return int(annotation)
        return annotation
