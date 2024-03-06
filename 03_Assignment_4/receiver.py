import sys
import tkinter as tk

data = sys.argv[1:]

# Open/create the file in write mode
with open("test.txt", "w") as file:
# Write some content to the file
    file.write(data)

