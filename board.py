from tangoTimeLine import *
import tkinter as tk
import time

def main():

    windowWidth = 1100
    windowHeight = 600

    command_template_top_left_corner_x_cor = windowWidth*0.05
    command_template_bottom_right_corner_x_cor = windowWidth*0.18

    command_template_height = windowHeight*0.1
    heightOffSet = windowHeight*0.05

    commandTemplatePositions = {"MoveForward": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.2,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.2-command_template_height, "color": "blue"},
                                "Turn": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.3,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.3-command_template_height, "color": "green"},
                                "TiltHead": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.4,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.4-command_template_height, "color": "yellow"},
                                "PanHead": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.5,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.5-command_template_height, "color": "pink"},
                                "TurnWaist": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.6,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.6-command_template_height, "color": "red"},
                                "WaitForSpeech": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.7,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.7-command_template_height, "color": "purple"},
                                "Talk": {"top_left_x": command_template_top_left_corner_x_cor, "top_left_y": windowHeight*0.8,
                                                "bottom_right_x": command_template_bottom_right_corner_x_cor,
                                                "bottom_right_y": windowHeight*0.8-command_template_height, "color": "orange"}}
    
    root = tk.Tk()
    root.title("Robot GUI")
    root.geometry(str(windowWidth) + "x" + str(windowHeight))
    board = tk.Canvas(root, width=windowWidth, height=windowHeight, bg="white")
    board.pack()
    timeLineContainer = tk.Canvas(board, width=windowWidth, height=windowHeight, bg='white')
    timeLineContainer.pack(side="right", fill="both", expand=True)
    sidebar = tk.Canvas(board, width=(windowWidth/4.5), bg='gray')
    sidebar.pack(side="left", fill="y")

    mf = MoveForward("MoveForward", "/iconFilePath", board, commandTemplatePositions)
    tu = Turn("Turn", "/iconFilePath", board, commandTemplatePositions)
    th = TiltHead("TiltHead", "/iconFilePath", board, commandTemplatePositions)
    ph = PanHead("PanHead", "/iconFilePath", board, commandTemplatePositions)
    tw = TurnWaist("TurnWaist", "/iconFilePath", board, commandTemplatePositions)
    wfS = WaitForSpeech("WaitForSpeech", "/iconFilePath", board, commandTemplatePositions)
    ta = Talk("Talk", "/iconFilePath", board, commandTemplatePositions)










    root.mainloop()

if __name__ == "__main__":
    main()