from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__()
        self.title = title
        self.iconFilePath = iconFilePath
        self.parameters = {}
        self.canvas = canvas
        self.positions = positions
        print("Let's make a rectangle!")
        positionSet = positions[self.title]
        rect = self.canvas.create_rectangle(positionSet["top_left_x"], positionSet["top_left_y"], positionSet["bottom_right_x"], positionSet["bottom_right_y"], fill=positionSet["color"])
        self.canvas.tag_bind(rect, '<Button-1>', self.on_click)
        self.canvas.tag_bind(rect, '<B1-Motion>', self.on_drag)

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


    def __str__(self):
        return self.title + ": " + str(self.parameters)

    @abstractmethod
    def doBehavior(self):
        pass

    def setParameter(self, key, value):
        self.parameters[key] = value

    def getParameters(self) -> dict:
        return self.parameters
    
    def getFilePath(self) -> str:
        return self.iconFilePath


class MoveForward(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        print("I am behaving!")


class Turn(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        pass


class TiltHead(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        pass


class PanHead(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    def doBehavior(self):
        #Movement instructions go here
        pass


class TurnWaist(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        pass


class WaitForSpeech(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        pass


class Talk(Command):
    def __init__(self, title, iconFilePath, canvas, positions):
        super().__init__(title, iconFilePath, canvas, positions)
    
    def doBehavior(self):
        #Movement instructions go here
        pass


class TimeLine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.commands = ["0", "0", "0", "0", "0", "0", "0", "0"]  # Will be a running list of Command objects to be iterated over when the "Start" button is hit.

    def populateItemFrames(self):
        pass

    def createSideBar(self):
        pass

    def runActiveCommands(self):
        for comm in self.commands:
            if comm != "0":
                comm.doBehavior()

    def addCommand(self, comm, position):
        self.commands[position] = comm

    def removeCommand(self, position):
        self.commands[position] = "0"

    def modifyCommandParameters(self, position, key, value):
        self.commands[position].setParameter(key, value)

    def mainloop(self):
        pass
    
