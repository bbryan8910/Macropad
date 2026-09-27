import board
import busio
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

# -------------------------------------------------------------
# 1. OLED DISPLAY SETUP (128x32 SSD1306)
# -------------------------------------------------------------
displayio.release_displays()

i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

# Force 180-degree rotation directly at initialization
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32, rotation=180)

splash = displayio.Group()

# Try loading the 1-bit BMP image
try:
    bitmap = displayio.OnDiskBitmap("/logo.bmp")
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    splash.append(tile_grid)
except Exception:
    # Fallback to text if logo.bmp is missing, wrong color depth, or invalid
    text_area = label.Label(terminalio.FONT, text="BBBRYAN8910", x=0, y=8)
    splash.append(text_area)
    sub_text = label.Label(terminalio.FONT, text="MACROPAD!", x=0, y=24)
    splash.append(sub_text)

display.root_group = splash

# -------------------------------------------------------------
# 2. KMK KEYBOARD INITIALIZATION
# -------------------------------------------------------------
keyboard = KMKKeyboard()

# -------------------------------------------------------------
# 3. KEY MATRIX SETUP (3x3 Grid)
# -------------------------------------------------------------
keyboard.col_pins = (board.D7, board.D8, board.D9)
keyboard.row_pins = (board.D2, board.D3, board.D6)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

# -------------------------------------------------------------
# 4. ROTARY ENCODER & MEDIA KEYS
# -------------------------------------------------------------
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.D0, board.D1, board.D10, False),
)

ENCODER_PRESS = KC.LCTRL(KC.LSHIFT(KC.BSPC))

encoder_handler.map = [
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, ENCODER_PRESS),),
]

# -------------------------------------------------------------
# 5. KEYMAP (Ctrl + Shift + 1 through 9)
# -------------------------------------------------------------
keyboard.keymap = [
    [
        KC.LCTRL(KC.LSHIFT(KC.N1)), KC.LCTRL(KC.LSHIFT(KC.N2)), KC.LCTRL(KC.LSHIFT(KC.N3)),
        KC.LCTRL(KC.LSHIFT(KC.N4)), KC.LCTRL(KC.LSHIFT(KC.N5)), KC.LCTRL(KC.LSHIFT(KC.N6)),
        KC.LCTRL(KC.LSHIFT(KC.N7)), KC.LCTRL(KC.LSHIFT(KC.N8)), KC.LCTRL(KC.LSHIFT(KC.N9)),
    ]
]

# -------------------------------------------------------------
# 6. START KMK
# -------------------------------------------------------------
if __name__ == '__main__':
    keyboard.go()
