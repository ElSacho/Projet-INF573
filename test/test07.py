import Quartz
import time
import pyautogui

def _normalKeyEvent(key, upDown):
    assert upDown in ('up', 'down'), "upDown argument must be 'up' or 'down'"

    try:
        if pyautogui.isShiftCharacter(key):
            key_code = keyboardMapping[key.lower()]

            event = Quartz.CGEventCreateKeyboardEvent(None,
                        keyboardMapping['shift'], upDown == 'down')
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            # Tiny sleep to let OS X catch up on us pressing shift
            time.sleep(0.01)

        else:
            key_code = keyboardMapping[key]

        event = Quartz.CGEventCreateKeyboardEvent(None, key_code, upDown == 'down')
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        time.sleep(0.01)

    # TODO - wait, is the shift key's keyup not done?
    # TODO - get rid of this try-except.

    except KeyError:
        raise RuntimeError("Key %s not implemented." % (key))