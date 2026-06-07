from enum import Enum, auto
from pynput import keyboard
from scrcpy_client.android_def import AKeyCode
from scrcpy_client.hid_def import HIDKeymod
from scrcpy_client.sdl_def import SDL_Scancode

class ControlMsgType(Enum):
    """
    Represents the types of control messages.
    """
    MSG_TYPE_INJECT_KEYCODE = 0
    MSG_TYPE_INJECT_TEXT = auto()
    MSG_TYPE_INJECT_TOUCH_EVENT = auto()
    MSG_TYPE_INJECT_SCROLL_EVENT = auto()
    MSG_TYPE_BACK_OR_SCREEN_ON = auto()
    MSG_TYPE_EXPAND_NOTIFICATION_PANEL = auto()
    MSG_TYPE_EXPAND_SETTINGS_PANEL = auto()
    MSG_TYPE_COLLAPSE_PANELS = auto()
    MSG_TYPE_GET_CLIPBOARD = auto()
    MSG_TYPE_SET_CLIPBOARD = auto()
    MSG_TYPE_SET_SCREEN_POWER_MODE = auto()
    MSG_TYPE_ROTATE_DEVICE = auto()
    MSG_TYPE_UHID_CREATE = auto()
    MSG_TYPE_UHID_INPUT = auto()
    MSG_TYPE_UHID_DESTROY = auto()
    MSG_TYPE_OPEN_HARD_KEYBOARD_SETTINGS = auto()

Key = keyboard.Key
KeyCode = keyboard.KeyCode
GenericKey = SDL_Scancode | HIDKeymod | AKeyCode

key_scancode_vk_map: dict[int, GenericKey] = {
    48: SDL_Scancode.SDL_SCANCODE_0,
    49: SDL_Scancode.SDL_SCANCODE_1,
    50: SDL_Scancode.SDL_SCANCODE_2,
    51: SDL_Scancode.SDL_SCANCODE_3,
    52: SDL_Scancode.SDL_SCANCODE_4,
    53: SDL_Scancode.SDL_SCANCODE_5,
    54: SDL_Scancode.SDL_SCANCODE_6,
    55: SDL_Scancode.SDL_SCANCODE_7,
    56: SDL_Scancode.SDL_SCANCODE_8,
    57: SDL_Scancode.SDL_SCANCODE_9,

    65: SDL_Scancode.SDL_SCANCODE_A,
    66: SDL_Scancode.SDL_SCANCODE_B,
    67: SDL_Scancode.SDL_SCANCODE_C,
    68: SDL_Scancode.SDL_SCANCODE_D,
    69: SDL_Scancode.SDL_SCANCODE_E,
    70: SDL_Scancode.SDL_SCANCODE_F,
    71: SDL_Scancode.SDL_SCANCODE_G,
    72: SDL_Scancode.SDL_SCANCODE_H,
    73: SDL_Scancode.SDL_SCANCODE_I,
    74: SDL_Scancode.SDL_SCANCODE_J,
    75: SDL_Scancode.SDL_SCANCODE_K,
    76: SDL_Scancode.SDL_SCANCODE_L,
    77: SDL_Scancode.SDL_SCANCODE_M,
    78: SDL_Scancode.SDL_SCANCODE_N,
    79: SDL_Scancode.SDL_SCANCODE_O,
    80: SDL_Scancode.SDL_SCANCODE_P,
    81: SDL_Scancode.SDL_SCANCODE_Q,
    82: SDL_Scancode.SDL_SCANCODE_R,
    83: SDL_Scancode.SDL_SCANCODE_S,
    84: SDL_Scancode.SDL_SCANCODE_T,
    85: SDL_Scancode.SDL_SCANCODE_U,
    86: SDL_Scancode.SDL_SCANCODE_V,
    87: SDL_Scancode.SDL_SCANCODE_W,
    88: SDL_Scancode.SDL_SCANCODE_X,
    89: SDL_Scancode.SDL_SCANCODE_Y,
    90: SDL_Scancode.SDL_SCANCODE_Z,

    37: SDL_Scancode.SDL_SCANCODE_LEFT,
    38: SDL_Scancode.SDL_SCANCODE_UP,
    39: SDL_Scancode.SDL_SCANCODE_RIGHT,
    40: SDL_Scancode.SDL_SCANCODE_DOWN,

    8: SDL_Scancode.SDL_SCANCODE_BACKSPACE,
    9: SDL_Scancode.SDL_SCANCODE_TAB,
    13: SDL_Scancode.SDL_SCANCODE_RETURN,
    20: SDL_Scancode.SDL_SCANCODE_CAPSLOCK,
    27: SDL_Scancode.SDL_SCANCODE_ESCAPE,
    32: SDL_Scancode.SDL_SCANCODE_SPACE,
    45: SDL_Scancode.SDL_SCANCODE_INSERT,
    46: SDL_Scancode.SDL_SCANCODE_DELETE,

    96: SDL_Scancode.SDL_SCANCODE_KP_0,
    97: SDL_Scancode.SDL_SCANCODE_KP_1,
    98: SDL_Scancode.SDL_SCANCODE_KP_2,
    99: SDL_Scancode.SDL_SCANCODE_KP_3,
    100: SDL_Scancode.SDL_SCANCODE_KP_4,
    101: SDL_Scancode.SDL_SCANCODE_KP_5,
    102: SDL_Scancode.SDL_SCANCODE_KP_6,
    103: SDL_Scancode.SDL_SCANCODE_KP_7,
    104: SDL_Scancode.SDL_SCANCODE_KP_8,
    105: SDL_Scancode.SDL_SCANCODE_KP_9,
    106: SDL_Scancode.SDL_SCANCODE_KP_MULTIPLY,
    107: SDL_Scancode.SDL_SCANCODE_KP_PLUS,
    109: SDL_Scancode.SDL_SCANCODE_KP_MINUS,
    110: SDL_Scancode.SDL_SCANCODE_KP_PERIOD,
    111: SDL_Scancode.SDL_SCANCODE_KP_DIVIDE,
    144: SDL_Scancode.SDL_SCANCODE_NUMLOCKCLEAR,

    160: HIDKeymod.HID_MOD_LEFT_SHIFT,
    161: HIDKeymod.HID_MOD_RIGHT_SHIFT,
    162: HIDKeymod.HID_MOD_LEFT_CONTROL,
    163: HIDKeymod.HID_MOD_RIGHT_CONTROL,
    164: HIDKeymod.HID_MOD_LEFT_ALT,
    165: HIDKeymod.HID_MOD_ALT_GR,

    112: AKeyCode.AKEYCODE_APP_SWITCH, # F1
    113: AKeyCode.AKEYCODE_HOME,
    114: AKeyCode.AKEYCODE_BACK,
    115: AKeyCode.AKEYCODE_MEDIA_PREVIOUS,
    116: AKeyCode.AKEYCODE_MEDIA_PLAY_PAUSE, # F5
    117: AKeyCode.AKEYCODE_MEDIA_NEXT,
    118: AKeyCode.AKEYCODE_VOLUME_DOWN,
    119: AKeyCode.AKEYCODE_VOLUME_UP,
    120: AKeyCode.AKEYCODE_BRIGHTNESS_DOWN,
    121: AKeyCode.AKEYCODE_BRIGHTNESS_UP, # F10
    122: AKeyCode.AKEYCODE_SOFT_SLEEP,
    123: AKeyCode.AKEYCODE_WAKEUP, # F12

    186: SDL_Scancode.SDL_SCANCODE_SEMICOLON,    # VK_OEM_1
    187: SDL_Scancode.SDL_SCANCODE_EQUALS,       # VK_OEM_PLUS
    188: SDL_Scancode.SDL_SCANCODE_COMMA,        # VK_OEM_COMMA
    189: SDL_Scancode.SDL_SCANCODE_MINUS,        # VK_OEM_MINUS
    190: SDL_Scancode.SDL_SCANCODE_PERIOD,       # VK_OEM_PERIOD
    191: SDL_Scancode.SDL_SCANCODE_SLASH,        # VK_OEM_2
    192: SDL_Scancode.SDL_SCANCODE_GRAVE,        # VK_OEM_3
    219: SDL_Scancode.SDL_SCANCODE_LEFTBRACKET,  # VK_OEM_4
    220: SDL_Scancode.SDL_SCANCODE_BACKSLASH,    # VK_OEM_5
    221: SDL_Scancode.SDL_SCANCODE_RIGHTBRACKET, # VK_OEM_6
    222: SDL_Scancode.SDL_SCANCODE_APOSTROPHE,   # VK_OEM_7
    226: SDL_Scancode.SDL_SCANCODE_NONUSBACKSLASH,
}

key_scancode_map: dict[Key | KeyCode, GenericKey] = {
    KeyCode.from_char("0"): SDL_Scancode.SDL_SCANCODE_0,
    KeyCode.from_char("1"): SDL_Scancode.SDL_SCANCODE_1,
    KeyCode.from_char("2"): SDL_Scancode.SDL_SCANCODE_2,
    KeyCode.from_char("3"): SDL_Scancode.SDL_SCANCODE_3,
    KeyCode.from_char("4"): SDL_Scancode.SDL_SCANCODE_4,
    KeyCode.from_char("5"): SDL_Scancode.SDL_SCANCODE_5,
    KeyCode.from_char("6"): SDL_Scancode.SDL_SCANCODE_6,
    KeyCode.from_char("7"): SDL_Scancode.SDL_SCANCODE_7,
    KeyCode.from_char("8"): SDL_Scancode.SDL_SCANCODE_8,
    KeyCode.from_char("9"): SDL_Scancode.SDL_SCANCODE_9,

    KeyCode.from_char("a"): SDL_Scancode.SDL_SCANCODE_A,
    KeyCode.from_char("b"): SDL_Scancode.SDL_SCANCODE_B,
    KeyCode.from_char("c"): SDL_Scancode.SDL_SCANCODE_C,
    KeyCode.from_char("d"): SDL_Scancode.SDL_SCANCODE_D,
    KeyCode.from_char("e"): SDL_Scancode.SDL_SCANCODE_E,
    KeyCode.from_char("f"): SDL_Scancode.SDL_SCANCODE_F,
    KeyCode.from_char("g"): SDL_Scancode.SDL_SCANCODE_G,
    KeyCode.from_char("h"): SDL_Scancode.SDL_SCANCODE_H,
    KeyCode.from_char("i"): SDL_Scancode.SDL_SCANCODE_I,
    KeyCode.from_char("j"): SDL_Scancode.SDL_SCANCODE_J,
    KeyCode.from_char("k"): SDL_Scancode.SDL_SCANCODE_K,
    KeyCode.from_char("l"): SDL_Scancode.SDL_SCANCODE_L,
    KeyCode.from_char("m"): SDL_Scancode.SDL_SCANCODE_M,
    KeyCode.from_char("n"): SDL_Scancode.SDL_SCANCODE_N,
    KeyCode.from_char("o"): SDL_Scancode.SDL_SCANCODE_O,
    KeyCode.from_char("p"): SDL_Scancode.SDL_SCANCODE_P,
    KeyCode.from_char("q"): SDL_Scancode.SDL_SCANCODE_Q,
    KeyCode.from_char("r"): SDL_Scancode.SDL_SCANCODE_R,
    KeyCode.from_char("s"): SDL_Scancode.SDL_SCANCODE_S,
    KeyCode.from_char("t"): SDL_Scancode.SDL_SCANCODE_T,
    KeyCode.from_char("u"): SDL_Scancode.SDL_SCANCODE_U,
    KeyCode.from_char("v"): SDL_Scancode.SDL_SCANCODE_V,
    KeyCode.from_char("w"): SDL_Scancode.SDL_SCANCODE_W,
    KeyCode.from_char("x"): SDL_Scancode.SDL_SCANCODE_X,
    KeyCode.from_char("y"): SDL_Scancode.SDL_SCANCODE_Y,
    KeyCode.from_char("z"): SDL_Scancode.SDL_SCANCODE_Z,

    KeyCode.from_char(","): SDL_Scancode.SDL_SCANCODE_COMMA,
    KeyCode.from_char("."): SDL_Scancode.SDL_SCANCODE_PERIOD,
    KeyCode.from_char("`"): SDL_Scancode.SDL_SCANCODE_RIGHTBRACKET,
    KeyCode.from_char("´"): SDL_Scancode.SDL_SCANCODE_RIGHTBRACKET,
    KeyCode.from_char("ˋ"): SDL_Scancode.SDL_SCANCODE_RIGHTBRACKET,
    KeyCode.from_char("~"): SDL_Scancode.SDL_SCANCODE_BACKSLASH,
    KeyCode.from_char("^"): SDL_Scancode.SDL_SCANCODE_BACKSLASH,
    KeyCode.from_char("-"): SDL_Scancode.SDL_SCANCODE_SLASH,
    KeyCode.from_char("_"): SDL_Scancode.SDL_SCANCODE_SLASH,
    KeyCode.from_char("="): SDL_Scancode.SDL_SCANCODE_EQUALS,
    KeyCode.from_char("«"): SDL_Scancode.SDL_SCANCODE_EQUALS,
    KeyCode.from_char("»"): SDL_Scancode.SDL_SCANCODE_EQUALS,
    KeyCode.from_char("["): SDL_Scancode.SDL_SCANCODE_LEFTBRACKET,
    KeyCode.from_char("]"): SDL_Scancode.SDL_SCANCODE_RIGHTBRACKET,
    KeyCode.from_char("\\"): SDL_Scancode.SDL_SCANCODE_BACKSLASH,
    KeyCode.from_char(";"): SDL_Scancode.SDL_SCANCODE_SEMICOLON,
    KeyCode.from_char("ç"): SDL_Scancode.SDL_SCANCODE_SEMICOLON,
    KeyCode.from_char("Ç"): SDL_Scancode.SDL_SCANCODE_SEMICOLON,
    KeyCode.from_char("'"): SDL_Scancode.SDL_SCANCODE_MINUS,
    KeyCode.from_char("/"): SDL_Scancode.SDL_SCANCODE_SLASH,
    KeyCode.from_char("?"): SDL_Scancode.SDL_SCANCODE_MINUS,
    KeyCode.from_char("+"): SDL_Scancode.SDL_SCANCODE_LEFTBRACKET,
    KeyCode.from_char("*"): SDL_Scancode.SDL_SCANCODE_LEFTBRACKET,
    KeyCode.from_char("º"): SDL_Scancode.SDL_SCANCODE_APOSTROPHE,
    KeyCode.from_char("ª"): SDL_Scancode.SDL_SCANCODE_APOSTROPHE,

    Key.backspace: SDL_Scancode.SDL_SCANCODE_BACKSPACE,
    Key.tab:       SDL_Scancode.SDL_SCANCODE_TAB,
    Key.enter:     SDL_Scancode.SDL_SCANCODE_RETURN,
    Key.esc:       SDL_Scancode.SDL_SCANCODE_ESCAPE,
    Key.space:     SDL_Scancode.SDL_SCANCODE_SPACE,
    Key.caps_lock: SDL_Scancode.SDL_SCANCODE_CAPSLOCK,
    Key.insert:    SDL_Scancode.SDL_SCANCODE_INSERT,
    Key.delete:    SDL_Scancode.SDL_SCANCODE_DELETE,
    Key.home:      SDL_Scancode.SDL_SCANCODE_HOME,
    Key.end:       SDL_Scancode.SDL_SCANCODE_END,
    Key.page_up:   SDL_Scancode.SDL_SCANCODE_PAGEUP,
    Key.page_down: SDL_Scancode.SDL_SCANCODE_PAGEDOWN,
    Key.left:      SDL_Scancode.SDL_SCANCODE_LEFT,
    Key.up:        SDL_Scancode.SDL_SCANCODE_UP,
    Key.right:     SDL_Scancode.SDL_SCANCODE_RIGHT,
    Key.down:      SDL_Scancode.SDL_SCANCODE_DOWN,

    Key.alt:     HIDKeymod.HID_MOD_ALT,
    Key.alt_l:   HIDKeymod.HID_MOD_LEFT_ALT,
    Key.alt_r:   HIDKeymod.HID_MOD_ALT_GR,
    Key.alt_gr:  HIDKeymod.HID_MOD_ALT_GR,
    Key.ctrl:    HIDKeymod.HID_MOD_CONTROL,
    Key.ctrl_l:  HIDKeymod.HID_MOD_LEFT_CONTROL,
    Key.ctrl_r:  HIDKeymod.HID_MOD_RIGHT_CONTROL,
    Key.shift:   HIDKeymod.HID_MOD_SHIFT,
    Key.shift_l: HIDKeymod.HID_MOD_LEFT_SHIFT,
    Key.shift_r: HIDKeymod.HID_MOD_RIGHT_SHIFT,
    Key.cmd:     HIDKeymod.HID_MOD_LEFT_GUI,
    Key.cmd_l:   HIDKeymod.HID_MOD_LEFT_GUI,
    Key.cmd_r:   HIDKeymod.HID_MOD_RIGHT_GUI,

    KeyCode.from_vk(37): SDL_Scancode.SDL_SCANCODE_LEFT,
    KeyCode.from_vk(38): SDL_Scancode.SDL_SCANCODE_UP,
    KeyCode.from_vk(39): SDL_Scancode.SDL_SCANCODE_RIGHT,
    KeyCode.from_vk(40): SDL_Scancode.SDL_SCANCODE_DOWN,

    KeyCode.from_vk(8 ): SDL_Scancode.SDL_SCANCODE_BACKSPACE,
    KeyCode.from_vk(9 ): SDL_Scancode.SDL_SCANCODE_TAB,
    KeyCode.from_vk(13): SDL_Scancode.SDL_SCANCODE_RETURN,
    KeyCode.from_vk(20): SDL_Scancode.SDL_SCANCODE_CAPSLOCK,
    KeyCode.from_vk(27): SDL_Scancode.SDL_SCANCODE_ESCAPE,
    KeyCode.from_vk(32): SDL_Scancode.SDL_SCANCODE_SPACE,
    KeyCode.from_vk(45): SDL_Scancode.SDL_SCANCODE_INSERT,
    KeyCode.from_vk(46): SDL_Scancode.SDL_SCANCODE_DELETE,

    KeyCode.from_vk(112): AKeyCode.AKEYCODE_APP_SWITCH, # F1
    KeyCode.from_vk(113): AKeyCode.AKEYCODE_HOME,
    KeyCode.from_vk(114): AKeyCode.AKEYCODE_BACK,
    KeyCode.from_vk(115): AKeyCode.AKEYCODE_MEDIA_PREVIOUS,
    KeyCode.from_vk(116): AKeyCode.AKEYCODE_MEDIA_PLAY_PAUSE, # F5
    KeyCode.from_vk(117): AKeyCode.AKEYCODE_MEDIA_NEXT,
    KeyCode.from_vk(118): AKeyCode.AKEYCODE_VOLUME_DOWN,
    KeyCode.from_vk(119): AKeyCode.AKEYCODE_VOLUME_UP,
    KeyCode.from_vk(120): AKeyCode.AKEYCODE_BRIGHTNESS_DOWN,
    KeyCode.from_vk(121): AKeyCode.AKEYCODE_BRIGHTNESS_UP, # F10
    KeyCode.from_vk(122): AKeyCode.AKEYCODE_SOFT_SLEEP,
    KeyCode.from_vk(123): AKeyCode.AKEYCODE_WAKEUP, # F12
}

def get_generic_key(k: Key | KeyCode) -> GenericKey | None:
    if isinstance(k, KeyCode):
        if k.char is not None and not k.char.isalnum():
            generic_key = key_scancode_map.get(KeyCode.from_char(k.char))
            if generic_key is not None:
                return generic_key
        generic_key = key_scancode_vk_map.get(k.vk)
        if generic_key is not None:
            return generic_key
    return key_scancode_map.get(k)
