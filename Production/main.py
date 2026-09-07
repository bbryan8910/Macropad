import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

# Modules for Consumer Control (Volume) & Encoder
from kmk.modules.consumer_control import ConsumerControl
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()

# -------------------------------------------------------------
# 1. MATRIX CONFIGURATION
# -------------------------------------------------------------
# Columns (Switch Pin 1s connected vertically): D7, D8, D9
keyboard.col_pins = (board.D7, board.D8, board.D9)

# Rows (Diode Cathodes connected horizontally): D2, D3, D6
keyboard.row_pins = (board.D2, board.D3, board.D6)

# Diode direction: Current flows from Switch Pin 1 (Cols) -> Pin 2 -> Diode Cathode (Rows)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Enable Media / Consumer Keys
consumer_control = ConsumerControl()
keyboard.modules.append(consumer_control)

# -------------------------------------------------------------
# 2. ROTARY ENCODER CONFIGURATION
# -------------------------------------------------------------
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# Rotary Encoder Pins: Pin A (CLK) = D0, Pin B (DT) = D1
encoder_handler.pins = (
    (board.D0, board.D1, None),
)

# Encoder Rotation: Counter-Clockwise = Volume Down, Clockwise = Volume Up
encoder_handler.map = [
    ((KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP),),
]

# -------------------------------------------------------------
# 3. KEYMAP DEFINITION
# -------------------------------------------------------------
# Mic Mute Shortcut for SW10 Push Switch (D10): Ctrl + Alt + Shift + M
# (Set this exact hotkey combination in Discord / OBS / Windows for Mic Mute)
MIC_MUTE = KC.LCTRL(KC.LALT(KC.LSHIFT(KC.M)))

keyboard.keymap = [
    [
        # --- 3x3 Key Matrix (SW1 - SW9) ---
        KC.F13, KC.F14, KC.F15,  # SW1, SW2, SW3
        KC.F16, KC.F17, KC.F18,  # SW4, SW5, SW6
        KC.F19, KC.F20, KC.F21,  # SW7, SW8, SW9
        
        # --- Rotary Encoder Switch (SW10) ---
        MIC_MUTE,               # Standalone Switch on D10
    ]
]

# Direct pin routing for the standalone encoder button (SW10 connected to D10)
# Note: In KMK, direct pins are appended to the matrix keymap as additional keys.
keyboard.direct_pins = [board.D10]

if __name__ == '__main__':
    keyboard.go()
