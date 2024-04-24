from tangoTimeLine import *
from StartButton import *
import tkinter as tk
import time
from maestro import *

class Overseer():
    def __init__(self) -> None:
        self.commands = []
        self.potentialRectangles = []
        self.tl = TimeLine()
        self.tango = Controller()

        self.windowWidth = 1100
        self.windowHeight = 600

        self.command_template_top_left_corner_x_cor = self.windowWidth*0.05
        self.command_template_bottom_right_corner_x_cor = self.windowWidth*0.18

        self.command_template_height = self.windowHeight*0.1

        self.commandTemplatePositions = {"MoveForward": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.2,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.2-self.command_template_height, "color": "blue"},
                                    "Turn": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.3,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.3-self.command_template_height, "color": "green"},
                                    "TiltHead": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.4,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.4-self.command_template_height, "color": "yellow"},
                                    "PanHead": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.5,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.5-self.command_template_height, "color": "pink"},
                                    "TurnWaist": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.6,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.6-self.command_template_height, "color": "red"},
                                    "WaitForSpeech": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.7,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.7-self.command_template_height, "color": "purple"},
                                    "Talk": {"top_left_x": self.command_template_top_left_corner_x_cor, "top_left_y": self.windowHeight*0.8,
                                                    "bottom_right_x": self.command_template_bottom_right_corner_x_cor,
                                                    "bottom_right_y": self.windowHeight*0.8-self.command_template_height, "color": "orange"}}
        
        self.root = tk.Tk()
        self.root.title("Robot GUI")
        self.root.geometry(str(self.windowWidth) + "x" + str(self.windowHeight))
        self.board = tk.Canvas(self.root, width=self.windowWidth, height=self.windowHeight, bg="white")
        self.board.pack()

        self.makeBoard()
        self.root.mainloop()

        # Reset the text file
        f = open("events.txt", "w")
        f.write("none,none,none,none,none,none,none,none")
        f.close()
        f = open("eventParameters.txt", "w")
        f.write("{"+"},{"+"},{"+"},{"+"},{"+"},{"+"},{"+"},{"+"}")
        f.close()
        f = open("rectangles.txt", "w")
        f.close()

    def runActiveCommands(self, event):
        print("--------------------------------------------------------------------")
        self.tl.runActiveCommands(self.commands)

    def resetBoard(self, event):
        f = open("events.txt", "w")
        f.write("none,none,none,none,none,none,none,none")
        f.close()
        f = open("eventParameters.txt", "w")
        f.write("{"+"},{"+"},{"+"},{"+"},{"+"},{"+"},{"+"},{"+"}")
        f.close()
        f2 = open("rectangles.txt", "r")
        rectangleList = f2.read().split(",")
        for num in rectangleList:
            if num != "":
                self.board.delete(int(num))
        self.tl.resetCommandList()
        self.makeCommandObjects()


    def openSettingsMenu(self, event, slotNum):
        f = open("events.txt", "r")
        objNameList = f.readline().split(",")
        titleOfCommandToEdit = objNameList[slotNum]
        for commObj in self.commands:
            if commObj.title == titleOfCommandToEdit:
                commObj.showOptions(slotNum)


    def makeCommandObjects(self):
        # Make the commands
        mf = MoveForward("MoveForward", "/iconFilePath", self.board, 
                         self.commandTemplatePositions, self.potentialRectangles, self.tango)
        tu = Turn("Turn", "/iconFilePath", self.board, 
                  self.commandTemplatePositions, self.potentialRectangles, self.tango)
        th = TiltHead("TiltHead", "/iconFilePath", self.board, 
                      self.commandTemplatePositions, self.potentialRectangles, self.tango)
        ph = PanHead("PanHead", "/iconFilePath", self.board, 
                     self.commandTemplatePositions, self.potentialRectangles, self.tango)
        tw = TurnWaist("TurnWaist", "/iconFilePath", self.board, 
                       self.commandTemplatePositions, self.potentialRectangles, self.tango)
        wfS = WaitForSpeech("WaitForSpeech", "/iconFilePath", self.board, 
                            self.commandTemplatePositions, self.potentialRectangles, self.tango)
        ta = Talk("Talk", "/iconFilePath", self.board, 
                  self.commandTemplatePositions, self.potentialRectangles, self.tango)

        self.commands = [mf, tu, th, ph, tw, wfS, ta]


    def makeBoard(self):

        # Make the line that divides the place from where the commands originate from the timeline
        self.board.create_line(self.command_template_top_left_corner_x_cor + 265, self.windowHeight, self.command_template_top_left_corner_x_cor + 265, 0)

        # Make the start button
        startbtn = self.board.create_rectangle(700, 450, 900, 550, fill="lightGreen")
        text = self.board.create_text(800, 500, text="START", fill="black", font=("Helvetica 15 bold"))
        self.board.tag_bind(startbtn, '<Button-1>', self.runActiveCommands)
        self.board.tag_bind(text, '<Button-1>', self.runActiveCommands)

        # Make reset button
        resetbtn = self.board.create_rectangle(400, 450, 600, 550, fill="#db2a33")
        text2 = self.board.create_text(500, 500, text="RESET", fill="black", font=("Helvetica 15 bold"))
        self.board.tag_bind(resetbtn, '<Button-1>', self.resetBoard)
        self.board.tag_bind(text2, '<Button-1>', self.resetBoard)

        time_line_slot_top_left_y = self.windowHeight*0.25
        time_line_slot_bottom_right_y = time_line_slot_top_left_y + 60

        # Top Row
        slot1 = self.board.create_rectangle(self.windowWidth*0.30, time_line_slot_top_left_y, self.windowWidth*0.30+143, time_line_slot_bottom_right_y)
        slot2 = self.board.create_rectangle(self.windowWidth*0.45, time_line_slot_top_left_y, self.windowWidth*0.45+143, time_line_slot_bottom_right_y)
        slot3 = self.board.create_rectangle(self.windowWidth*0.60, time_line_slot_top_left_y, self.windowWidth*0.60+143, time_line_slot_bottom_right_y)
        slot4 = self.board.create_rectangle(self.windowWidth*0.75, time_line_slot_top_left_y, self.windowWidth*0.75+143, time_line_slot_bottom_right_y)
        # Bottom Row
        slot5 = self.board.create_rectangle(self.windowWidth*0.30, time_line_slot_top_left_y+100, self.windowWidth*0.30+143, time_line_slot_bottom_right_y+100)
        slot6 = self.board.create_rectangle(self.windowWidth*0.45, time_line_slot_top_left_y+100, self.windowWidth*0.45+143, time_line_slot_bottom_right_y+100)
        slot7 = self.board.create_rectangle(self.windowWidth*0.60, time_line_slot_top_left_y+100, self.windowWidth*0.60+143, time_line_slot_bottom_right_y+100)
        slot8 = self.board.create_rectangle(self.windowWidth*0.75, time_line_slot_top_left_y+100, self.windowWidth*0.75+143, time_line_slot_bottom_right_y+100)
        
        self.potentialRectangles = [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8]

        # Make the Labels for the commands
        self.board.create_text(250, 90, text="Move \nForward", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 150, text="Rotate", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 210, text="Tilt Head", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 270, text="Pan Head", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 330, text="Turn Waist", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 390, text="Wait For \nSpeech", fill="black", font=("Helvetica 12 bold"))
        self.board.create_text(250, 450, text="Talk", fill="black", font=("Helvetica 12 bold"))

        # Make the buttons that will open the options dialogue
        slot1Settings = self.board.create_rectangle(self.windowWidth*0.30, time_line_slot_top_left_y-55, self.windowWidth*0.30+100, time_line_slot_bottom_right_y-70, fill="grey")
        slot2Settings = self.board.create_rectangle(self.windowWidth*0.45, time_line_slot_top_left_y-55, self.windowWidth*0.45+100, time_line_slot_bottom_right_y-70, fill="grey")
        slot3Settings = self.board.create_rectangle(self.windowWidth*0.60, time_line_slot_top_left_y-55, self.windowWidth*0.60+100, time_line_slot_bottom_right_y-70, fill="grey")
        slot4Settings = self.board.create_rectangle(self.windowWidth*0.75, time_line_slot_top_left_y-55, self.windowWidth*0.75+100, time_line_slot_bottom_right_y-70, fill="grey")

        slot5Settings = self.board.create_rectangle(self.windowWidth*0.30, time_line_slot_top_left_y+180, self.windowWidth*0.30+100, time_line_slot_bottom_right_y+170, fill="grey")
        slot6Settings = self.board.create_rectangle(self.windowWidth*0.45, time_line_slot_top_left_y+180, self.windowWidth*0.45+100, time_line_slot_bottom_right_y+170, fill="grey")
        slot7Settings = self.board.create_rectangle(self.windowWidth*0.60, time_line_slot_top_left_y+180, self.windowWidth*0.60+100, time_line_slot_bottom_right_y+170, fill="grey")
        slot8Settings = self.board.create_rectangle(self.windowWidth*0.75, time_line_slot_top_left_y+180, self.windowWidth*0.75+100, time_line_slot_bottom_right_y+170, fill="grey")

        self.board.tag_bind(slot1Settings, '<Button-1>', lambda event, 
                            arg1=0: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot2Settings, '<Button-1>', lambda event, 
                            arg1=1: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot3Settings, '<Button-1>', lambda event, 
                            arg1=2: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot4Settings, '<Button-1>', lambda event, 
                            arg1=3: self.openSettingsMenu(event, arg1))

        self.board.tag_bind(slot5Settings, '<Button-1>', lambda event, 
                            arg1=4: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot6Settings, '<Button-1>', lambda event, 
                            arg1=5: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot7Settings, '<Button-1>', lambda event, 
                            arg1=6: self.openSettingsMenu(event, arg1))
        self.board.tag_bind(slot8Settings, '<Button-1>', lambda event, 
                            arg1=7: self.openSettingsMenu(event, arg1))

        self.makeCommandObjects()


o = Overseer()