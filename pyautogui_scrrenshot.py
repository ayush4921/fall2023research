import pyautogui
from PIL import ImageDraw

# Switch to Minecraft
pyautogui.hotkey(
    "command", "tab"
)  # Assumes Minecraft is the next application in the app switcher

# Take the first screenshot
screenshot1 = pyautogui.screenshot()

# Move the mouse by 100 pixels to the right
current_mouse_position = pyautogui.position()
pyautogui.moveTo(current_mouse_position.x + 100, current_mouse_position.y)

# Take the second screenshot
screenshot2 = pyautogui.screenshot()

# Draw a square around the middle of the first screenshot
width1, height1 = screenshot1.size
middle_x1, middle_y1 = width1 // 2, height1 // 2
draw1 = ImageDraw.Draw(screenshot1)
draw1.rectangle(
    [(middle_x1 - 50, middle_y1 - 50), (middle_x1 + 50, middle_y1 + 50)], outline="red"
)

# Draw a square 100 pixels to the right of the middle in the second screenshot
draw2 = ImageDraw.Draw(screenshot2)
draw2.rectangle(
    [(middle_x1 + 50, middle_y1 - 50), (middle_x1 + 150, middle_y1 + 50)], outline="red"
)

# Save the modified screenshots
screenshot1.save("screenshot1_modified.png")
screenshot2.save("screenshot2_modified.png")
