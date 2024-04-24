import tkinter as tk

class SliderWidget:
    def __init__(self, master, label, min_val, max_val, default_val):
        self.master = master
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        
        self.slider_label = tk.Label(master, text=label)
        self.slider_label.pack()
        
        self.slider = tk.Scale(master, from_=min_val, to=max_val, orient=tk.HORIZONTAL)
        self.slider.set(default_val)
        self.slider.pack()
    
    def get_value(self):
        return self.slider.get()
    
    def get_title(self):
        return self.label