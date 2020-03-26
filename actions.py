import keyboard

def release_key_if_pressed(key):
    if keyboard.is_pressed(key):
        keyboard.release(key)

def _gen_default_key_action(key):
    return (lambda: keyboard.press_and_release(key), lambda: keyboard.press(key), lambda: release_key_if_pressed(key))

names_and_actions = {
    #Action Name: (action_on_press, action_on_hold, action_on_release)
    'bkspace': _gen_default_key_action('backspace'),
    'play': (lambda: keyboard.press_and_release("play/pause media"), lambda: None, lambda: release_key_if_pressed("play/pause media")),
    'vol-': _gen_default_key_action("volume down"),
    'vol+': _gen_default_key_action("volume up"),
    '<-': _gen_default_key_action("previous track"),
    '->': _gen_default_key_action("next track"),

}

for key in 'abcdefghijklmnopqrstuvwxyz':
    names_and_actions[key] = _gen_default_key_action(key)

for key in '0123456789':
    names_and_actions[key] = _gen_default_key_action(key)

for key in ['space', 'enter', 'esc', 'backspace', 'del', 'tab']:
    names_and_actions[key] = _gen_default_key_action(key)

for key in ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']:
    names_and_actions[key] = _gen_default_key_action(key)


def get_actions_by_name(action_name):
    defined_actions = names_and_actions.get(action_name)
    if defined_actions:
        return defined_actions
    else:
        return (lambda: keyboard.write(action_name), lambda: keyboard.write(action_name), lambda: None)