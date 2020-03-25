# SquareBox PadBoard

# TODO doc
    - What is it -> OSK for gamepads (inspired by danzeff OSK for PSP)
    - Button and analogs mappings
    - Layout(s)
    - Only first controller (Plug&Play works)
    - Platform support
    - known issues
    - Controllers support (XBox One, XBox 360, Dualshock4 using DS4Window software)
    - How to get it and how to build it


Windows executable (.exe) in the dist folder of this repo ready to be downloaded and used.
> **NOTE:** the exe may be smaller but we didn't optimize the imported libraries yet.
> However, it's not a critical point at the moment as it is still a manageable 18MB-ish size

to rebuild the exe run:
`pyinstaller -F -w squarebox_padboard.py`
