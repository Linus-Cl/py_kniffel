class Button:

    def __init__(self, rect, text, color, hover_color, font) -> None:
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.disabled_color = "gray"
        self.hover = False
        self.disabled = False
        self.font = font
