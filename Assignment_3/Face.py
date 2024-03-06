import tkinter as tk
import threading
import math
import random
from time import sleep

class Face(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.canvas = tk.Canvas(self, bg='white')
        self.bind('<Escape>', lambda e: self.destroy())
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        # Eye attributes
        self.eye_radius = 80
        self.eye_size = 200
        self.eye_spacing = 300
        self.eye_color = 'black'
        self.pupil_radius = 40
        self.pupil_color = 'white'

        # Create eyes
        self.eye1_x = self.width // 2 - self.eye_spacing // 2
        self.eye1_y = self.height // 2
        self.eye2_x = self.width // 2 + self.eye_spacing // 2
        self.eye2_y = self.height // 2
        self.eye1 = self.canvas.create_oval(self.eye1_x - self.eye_size // 2, self.eye1_y - self.eye_size // 2,
                                            self.eye1_x + self.eye_size // 2, self.eye1_y + self.eye_size // 2,
                                            fill=self.eye_color, outline='')
        self.eye2 = self.canvas.create_oval(self.eye2_x - self.eye_size // 2, self.eye2_y - self.eye_size // 2,
                                            self.eye2_x + self.eye_size // 2, self.eye2_y + self.eye_size // 2,
                                            fill=self.eye_color, outline='')

        # Pupil parameters
        self.pupil1_x = self.eye1_x
        self.pupil1_y = self.eye1_y
        self.pupil2_x = self.eye2_x
        self.pupil2_y = self.eye2_y
        self.pupil1 = self.canvas.create_oval(self.pupil1_x - self.pupil_radius, self.pupil1_y - self.pupil_radius,
                                               self.pupil1_x + self.pupil_radius, self.pupil1_y + self.pupil_radius,
                                               fill=self.pupil_color, outline='')
        self.pupil2 = self.canvas.create_oval(self.pupil2_x - self.pupil_radius, self.pupil2_y - self.pupil_radius,
                                               self.pupil2_x + self.pupil_radius, self.pupil2_y + self.pupil_radius,
                                               fill=self.pupil_color, outline='')

        # Mouth parameters
        self.mouth_width = 150
        self.mouth_height = 100
        self.mouth_color = 'red'
        self.mouth_y = self.height // 2 + 150
        self.mouth = self.canvas.create_rectangle(self.width // 2 - self.mouth_width // 2,
                                                  self.mouth_y - self.mouth_height // 2,
                                                  self.width // 2 + self.mouth_width // 2,
                                                  self.mouth_y + self.mouth_height // 2,
                                                  fill=self.mouth_color, outline='')

        # Start threads for animations
        threading.Thread(target=self.move_pupils, daemon=True).start()
        threading.Thread(target=self.blink, daemon=True).start()
        threading.Thread(target=self.move_mouth, daemon=True).start()

        # Store original pupil positions
        self.original_pupil1_x = self.pupil1_x
        self.original_pupil1_y = self.pupil1_y
        self.original_pupil2_x = self.pupil2_x
        self.original_pupil2_y = self.pupil2_y

    def reset_pupils(self):
        self.canvas.coords(self.pupil1, self.original_pupil1_x - self.pupil_radius, self.original_pupil1_y - self.pupil_radius,
                           self.original_pupil1_x + self.pupil_radius, self.original_pupil1_y + self.pupil_radius)
        self.canvas.coords(self.pupil2, self.original_pupil2_x - self.pupil_radius, self.original_pupil2_y - self.pupil_radius,
                           self.original_pupil2_x + self.pupil_radius, self.original_pupil2_y + self.pupil_radius)

    def move_pupils(self):
        while True:
            # Randomly move pupils
            self.move_pupil(self.eye1, self.pupil1, self.eye1_x, self.eye1_y)
            self.move_pupil(self.eye2, self.pupil2, self.eye2_x, self.eye2_y)
            sleep(0.4)  # Adjust the speed of pupil movement here

    def move_pupil(self, eye, pupil, eye_x, eye_y):
        eye_x, eye_y = eye_x + self.eye_size // 2, eye_y + self.eye_size // 2
        pupil_x, pupil_y = self.canvas.coords(pupil)[0] + self.pupil_radius, self.canvas.coords(pupil)[1] + self.pupil_radius
        angle = math.atan2(eye_y - pupil_y, eye_x - pupil_x)
        distance = min(self.eye_size // 2 - self.pupil_radius, random.randint(10, 40))
        new_x = eye_x + (self.eye_size // 2 - self.eye_radius) * math.cos(angle)  # Ensuring pupil remains within the eye
        new_y = eye_y + (self.eye_size // 2 - self.eye_radius) * math.sin(angle)  # Ensuring pupil remains within the eye
        self.canvas.coords(pupil, new_x - self.pupil_radius, new_y - self.pupil_radius,
                           new_x + self.pupil_radius, new_y + self.pupil_radius)
        self.update()

    def blink(self):
        while True:
            # Close eyes
            for _ in range(5):
                self.canvas.coords(self.eye1, self.eye1_x - self.eye_size // 2, self.eye1_y - self.eye_radius // 2,
                                   self.eye1_x + self.eye_size // 2, self.eye1_y + self.eye_radius // 2)
                self.canvas.coords(self.eye2, self.eye2_x - self.eye_size // 2, self.eye2_y - self.eye_radius // 2,
                                   self.eye2_x + self.eye_size // 2, self.eye2_y + self.eye_radius // 2)
                self.reset_pupils()  # Reset pupils to original state
                self.update()
                sleep(0.05)

            # Open eyes
            for _ in range(5):
                self.canvas.coords(self.eye1, self.eye1_x - self.eye_size // 2, self.eye1_y - self.eye_size // 2,
                                   self.eye1_x + self.eye_size // 2, self.eye1_y + self.eye_size // 2)
                self.canvas.coords(self.eye2, self.eye2_x - self.eye_size // 2, self.eye2_y - self.eye_size // 2,
                                   self.eye2_x + self.eye_size // 2, self.eye2_y + self.eye_size // 2)
                self.update()
                sleep(0.05)

            sleep(random.uniform(1, 5))  # Random time before next blink

    def move_mouth(self):
        while True:
            # Adjust mouth height
            new_height = random.randint(10, 50)
            self.canvas.coords(self.mouth, self.width // 2 - self.mouth_width // 2,
                           self.mouth_y - new_height // 2,
                           self.width // 2 + self.mouth_width // 2,
                           self.mouth_y + new_height // 2)

            self.update()
            sleep(random.uniform(0.1, 1))  # Adjust the speed of mouth movement

if __name__ == "__main__":
    face = Face()
    face.bind('<t>', lambda e: face.move_mouth())
    face.bind('<y>', lambda e: face.blink())
    face.bind('<u>', lambda e: face.move_pupils())
    face.mainloop()
