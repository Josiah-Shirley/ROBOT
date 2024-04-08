import tkinter as tk

class DragDropRectangles:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=300, bg='white')
        self.canvas.pack(side="right", fill="both", expand=True)
        
        self.sidebar = tk.Frame(master, width=100, bg='lightgray')
        self.sidebar.pack(side="left", fill="y")
        
        self.rect1 = self.canvas.create_rectangle(50, 50, 150, 150, fill='blue')
        self.rect2 = self.canvas.create_rectangle(250, 50, 350, 150, fill='red')
        
        self.canvas.tag_bind(self.rect1, '<Button-1>', self.on_click)
        self.canvas.tag_bind(self.rect2, '<Button-1>', self.on_click)
        
        self.canvas.tag_bind(self.rect1, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.rect2, '<B1-Motion>', self.on_drag)
        
        self.drag_data = {'item': None, 'x': 0, 'y': 0}

    def on_click(self, event):
        self.drag_data['item'] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_drag(self, event):
        if self.drag_data['item']:
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            self.canvas.move(self.drag_data['item'], dx, dy)
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y

def main():
    root = tk.Tk()
    root.title("Drag and Drop Rectangles with Sidebar")
    app = DragDropRectangles(root)
    root.mainloop()

if __name__ == "__main__":
    main()
