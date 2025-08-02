import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import pygame
import threading
import random

# Constants
AVOID_DISTANCE = 150
MOVE_DISTANCE = 200
PET_SIZE = (100, 100)

# Setup main window
root = tk.Tk()
root.overrideredirect(True)  # No window borders
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")  # Make white color transparent

# Load and resize pet image
pet_image = Image.open("pet.png").resize(PET_SIZE, Image.LANCZOS)
pet_photo = ImageTk.PhotoImage(pet_image)

# Create a canvas with transparent background
canvas = tk.Canvas(root, width=PET_SIZE[0], height=PET_SIZE[1], bg="white", highlightthickness=0)
canvas.pack()

# Draw the pet
canvas.create_image(0, 0, anchor=tk.NW, image=pet_photo)

# Initialize pygame for sound
pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load("boing.mp3")
    pygame.mixer.music.play()

def move_pet_away():
    pet_x = root.winfo_x()
    pet_y = root.winfo_y()
    mouse_x, mouse_y = pyautogui.position()

    dx = pet_x - mouse_x
    dy = pet_y - mouse_y
    distance = (dx**2 + dy**2) ** 0.5

    if distance < AVOID_DISTANCE:
        # Move to a random direction
        new_x = pet_x + MOVE_DISTANCE * random.choice([-1, 1])
        new_y = pet_y + MOVE_DISTANCE * random.choice([-1, 1])

        # Stay within screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        new_x = max(0, min(screen_width - PET_SIZE[0], new_x))
        new_y = max(0, min(screen_height - PET_SIZE[1], new_y))

        root.geometry(f"+{int(new_x)}+{int(new_y)}")
        threading.Thread(target=play_sound, daemon=True).start()

    root.after(50, move_pet_away)

# Start checking the mouse
move_pet_away()

# Start in center
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root.geometry(f"+{screen_w // 2}+{screen_h // 2}")

# Run the app
root.mainloop()
