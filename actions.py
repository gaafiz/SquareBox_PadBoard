import keyboard

def release_key_if_pressed(key):
    if keyboard.is_pressed(key):
        keyboard.release(key)

def _gen_default_key_action(key):
    return (lambda: keyboard.press_and_release(key), lambda: keyboard.press(key), lambda: release_key_if_pressed(key))

names_and_actions = {
    #Action Name: (action_on_press, action_on_hold, action_on_release)
    'del': (lambda: keyboard.press('backspace'), lambda: keyboard.press('backspace'), lambda: release_key_if_pressed('backspace')),
}

for key in 'abcdefghijklmnopqrstuvwxyz':
    names_and_actions[key] = _gen_default_key_action(key)

for key in ['space', 'enter']:
    names_and_actions[key] = _gen_default_key_action(key)


def get_actions_by_name(action_name):
    defined_actions = names_and_actions.get(action_name)
    if defined_actions:
        return defined_actions
    else:
        return (lambda: keyboard.write(action_name), lambda: keyboard.write(action_name), lambda: None)