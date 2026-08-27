import os

import customtkinter as ctk
from PIL import Image


NAVY = "#111936"
NAVY_LIGHT = "#1D2A59"
GOLD = "#D6A83B"
GOLD_HOVER = "#B88B24"
CREAM = "#F8F3E7"
WHITE = "#FFFFFF"
MUTED = "#D7D9E5"
DANGER = "#B54848"
DANGER_HOVER = "#8E3030"
SUCCESS = "#2F8F67"
SUCCESS_HOVER = "#236C4E"

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "labajona_logo.jpg"
)


def logo_image(width, height):
    if not os.path.exists(LOGO_PATH):
        return None

    return ctk.CTkImage(
        light_image=Image.open(LOGO_PATH),
        dark_image=Image.open(LOGO_PATH),
        size=(width, height)
    )


def apply_theme():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
