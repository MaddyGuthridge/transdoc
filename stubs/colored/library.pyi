from dataclasses import dataclass

@dataclass
class Library:
    ESC: str = ...
    END: str = ...
    FOREGROUND_256: str = ...
    BACKGROUND_256: str = ...
    FOREGROUND_RGB: str = ...
    BACKGROUND_RGB: str = ...
    UNDERLINE_COLOR: str = ...
    CONTROLS = ...
    STYLES = ...
    COLORTERM = ...
    COLORS = ...
    HEX_COLORS = ...
    def __init__(self, ESC=..., END=..., FOREGROUND_256=..., BACKGROUND_256=..., FOREGROUND_RGB=..., BACKGROUND_RGB=..., UNDERLINE_COLOR=...) -> None: ...
