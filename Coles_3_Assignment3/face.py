import tkinter as tk

class Draw:

    def __int__(self):
        self.root = tk.Tk()
        self.root.attributes('fullscreen', True)
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("Motion", self.draw)
        self.root.mainloop()

    def draw(self, event):
        x_1, y_1 = (event.x - 1), (event.y - 1)
        x_2, y_2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x_1, y_1, x_2, y_2, fill="black", width=0)

if __name__ == "__main__":
    Draw()