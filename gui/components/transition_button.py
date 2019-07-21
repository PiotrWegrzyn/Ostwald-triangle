from kivy.uix.button import Button


class TransitionButton(Button):
    def __init__(self, **kwargs):
        self.transition = kwargs.pop("transition", None)
        self.transition_method = kwargs.pop("transition_method", None)
        super().__init__(**kwargs)



