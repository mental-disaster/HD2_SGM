from pynput import keyboard
from pynput.keyboard import Key, Controller

UP = Key.up
DOWN = Key.down
LEFT = Key.left
RIGHT = Key.right

combinations = {
    (Key.ctrl_l, '1'): [UP, DOWN, RIGHT, LEFT, UP],
    (Key.ctrl_l, '2'): [UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT],
    ('f',): [UP, DOWN, RIGHT, LEFT, UP]
}

current_keys = set()
active_combination = None

keyboard_controller = Controller()


def execute_sequence(keys):
    for key in keys:
        keyboard_controller.tap(key)


def on_press(key):
    global active_combination, current_keys

    key_char = getattr(key, 'char', None)

    if key_char:
        current_keys.add(key_char)
    else:
        current_keys.add(key)

    if active_combination is None:
        for combination, sequence in combinations.items():
            if all(k in current_keys for k in combination):
                execute_sequence(sequence)
                active_combination = combination
                break


def on_release(key):
    global active_combination, current_keys

    key_char = getattr(key, 'char', None)

    if key_char:
        current_keys.remove(key_char)
    else:
        current_keys.remove(key)

    if active_combination and all(k not in current_keys for k in active_combination):
        active_combination = None

    if key == Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()