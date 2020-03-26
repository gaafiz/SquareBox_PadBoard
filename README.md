# SquareBox the PadBoard

SquareBox the PadBoard gets you **full control of your PC using only a Gamepad**!
It allows you to **use keyboard hotkeys, write text and control the mouse with your Gamepad Controller** right there in your hands.

- Are you trying or thinking about building a pc to use as console or emulation station in your living room?
- Were you connecting your laptop to the TV, getting ready for watching a movie, when you realized you had no easy way to control your favorite media confortably from your bed?
- Are you playing your favorite game with your PS4 Controller and you need to write a quick message to your team buddy?

If the answer to at least one of these question is yes, then a small bluetooth touchpad + keyboard may solve your problems.
But, if your are ~~broke~~ lazy to buy it, good news! you can still solve your problems with SquareBox and your favourite Gamepad.

> **INFO**: Squarebox the Padboard is inspired by the PSP **Danzeff OSK** popular in the Homebrew scene of the (g)old times of PSP. Google it for reviving good memories.


## How to get SquareBox

> **DISCLAIMER**:
> At the moment, Squarebox **supports only Windows** and if 2 or more gamepads are connected, the first one will control the PadBoard.
> **Supported controllers**: Xbox 360, Xbox One, PS4 (if you install [DS4Windows](http://ds4windows.com/) driver)

You can download the last version of the Windows executable (.exe) [HERE](https://github.com/giulianfazio/SquareBox_PadBoard/blob/master/dist/squarebox_padboard.exe?raw=true).

Alternatively, if you don't trust the executable, you can easily build it yourself.
1. Install all necessary python packages listed in [requirementes.txt](/requirements.txt)
2. Run in the project folder the following command: `pyinstaller -F -w squarebox_padboard.py`
3. Enjoy your new exe placed in `dist/squarebox_padboard.exe`


## Main features

- **Control the keyboard** (press hotkeys, keys combinations and write text) with a combination of Analog stick + 4 main action buttons.
- **Control the mouse** with a combination of Analog stick + Arrow buttons.
- **Support rapid-fire**: if you keep a button pressed, it will repeat the expected action until the button is released
- **Gamepad Plug and Play**: the app instantly works everytime you connect your Gamepad (most importantly it doesn't crash when you disconnect the Gamepad :D)


## Gamepad mappings

Here you'll find a comprehensive list of all the buttons combos Squarebox the Padboard uses:

* **L1 + START + SELECT**: Hide (and disable) or Show (and re-enable) the PadBoard
* **D-Pad**: Simulate Keyboard directional arrows.
* **L-Stick**: Select 1 of the 9 boxes in the current padboard grill
* **X, Y, A, B (if you are using a Xbox controllerd)**: Press 1 of the 4 letters from the selected box
* **R-Stick**: Move the padboard on the screen
* **L1**: When pressed, shows the alternative grill of the current padboard layout.
* **L2**: Equal to press ALT on a Keyboard
* **R2**: Equal to press CTRL on a Keyboard
* **R1**: Equal to press SHIFT on a Keyboard
* **L3**: Changes the current keyboard layout
* **R3**: Toggle the **Mouse Mode**

When the **Mouse mode** is active, this alternative combos are active:

* **D-Pad Left,Right**: Left or Right Mouse click
* **D-Pad Up, Down**: Mouse scroll Up or Down
* **R-Stick**: Move the mouse coursor (Slow and precise mode)
* **L1 + R-Stick**: Move the mouse cursor (Fast mode)

## To implement

* Configuration File (at least: custom keyboard sizes and custom keyboard layouts)
* Start on-Windows-startup option
* Make the keyboard moving only within the display boundaries
* Macros (in place of some letters) support
* Clean code! Espacially the input part (decouple input events from actual actions)

## Known Issues

* SquareBox cannot suppress Gamepad events. So, if another app (like steam) is using controller inputs, they will be both "doing stugg" reacting to the same controller inputs
* Spike in CPU usage when the keyboard windows is moving for > 20 secs. It shouldn't happen in normal usage as it mostrly happen when the R-Stick movements are spammed for long time (> 20 secs)
* Keyboard may appear too big on small screen or too small on big screens (will be solved by the "custom keyboard size" option)`
* Squarebox executable has a big size considering to the code used. This is likely due to the size of libraries imported used in the code. It's not a critical point at the moment as it is still a manageable 18MB-ish executable. But is something to have a look at.



