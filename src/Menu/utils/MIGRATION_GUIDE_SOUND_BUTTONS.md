# Migration Guide: Adding Sound to Buttons

This guide explains how to update your code to use the new sound-enabled buttons in the menu system.

## New Button Classes

Two new button classes have been added with built-in sound effects:

1. `SoundButton` - A text button with sound effects
2. `SoundImageButton` - An image button with sound effects

## How to Update Your Code

### 1. Update Imports

Change your imports from:

```python
from Menu.components.button import Button, ImageButton
```

to:

```python
from Menu.components.sound_button import SoundButton, SoundImageButton
```

### 2. Replace Button Creation

#### For Text Buttons:

Change:
```python
button = Button(x, y, width, height, "Button Text", font)
```

to:
```python
button = SoundButton(x, y, width, height, "Button Text", font)
```

#### For Image Buttons:

Change:
```python
button = ImageButton(x, y, image, scale=1.0)
```

to:
```python
button = SoundImageButton(x, y, image, scale=1.0)
```

## What's Different

- The new buttons automatically play a sound effect when clicked
- The sound is played before the button's callback is executed
- The sound will only play if the sound manager is properly set up
- If the sound manager is not available, the button will still function normally without sound

## Sound Customization

The sound effect is defined in `Menu/utils/sound_utils.py`. You can modify the `play_button_select()` function to change the sound effect or its behavior.

## Testing

After updating your code, test all buttons to ensure:
1. The sound plays when buttons are clicked
2. The button's original functionality remains the same
3. There are no errors if the sound system is not available
