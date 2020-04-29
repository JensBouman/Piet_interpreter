# helloworld.py
from time import sleep
import threading
import tkinter as tk
import pygubu

import interpreter.imageWrapper as imageWrapper
import interpreter.lexer as lexer
import interpreter.lexerTokens as lexerTokens
import interpreter.colors as colors
import interpreter.movement as movement
import interpreter.programState as programState
import interpreter.main as main
import threading

import infoManager
import canvasManager


class GUI:
    def __init__(self):
        # In pixelWidth/height per pixel. scaleSize = 25 means that every pixel will show as a 25x25 square
        self.scaleSize = 25
        # In percentage
        self.executionSpeed = 15

        # In seconds
        self.maxWait = 5

        self.image = None
        self.graph = None
        self.programState = None
        self.selectedPosition = None

        self.optionBar = None
        self.actionBar = None
        self.content = None
        self.canvas = None

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('../assets/tkinterLayout.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('rootWindow')

        self.initializeFrames()
        self.initializeCallbacks()
        self.infoManager = infoManager.infoManager(self.builder, self.generalInfoFrame, self.programStateInfoFrame)
        self.canvasManager = canvasManager.canvasManager(self.canvas, self.image, self.programState, self.scaleSize)


    def run(self):
        self.mainwindow.mainloop()


    def initializeCallbacks(self):
        self.builder.connect_callbacks({
            'loadFile': self.loadFile,
            'setScale': self.setScale,
            'takeStep': self.takeStep,
            'setExecutionSpeed': self.setExecutionSpeed,
            'setBreakpoint': self.setBreakpoint,
            'runProgram': self.runProgram
        })

        self.canvas.bind("<Button-1>", self.canvasPressed)

    def initializeFrames(self):
        self.optionBar = self.builder.get_object('optionBar', self.mainwindow)
        self.content = self.builder.get_object('content', self.mainwindow)
        self.actionBar = self.builder.get_object('actionBar', self.mainwindow)
        self.generalInfoFrame = self.builder.get_object("generalInfoFrame", self.content)
        self.programStateInfoFrame = self.builder.get_object("programStateInfoFrame", self.content)
        canvasFrame = self.builder.get_object('canvasFrame', self.content)
        self.canvas = self.builder.get_object('canvas', canvasFrame)


    def update(self):
        self.infoManager.updateInfo(self.image, self.graph, self.programState)
        self.canvasManager.updateScaleSize(self.scaleSize)
        self.canvasManager.updateImage(self.image)
        self.canvasManager.updateProgramState(self.programState)
        self.canvasManager.updateCanvas()


    def takeStep(self):
        if self.image is None or self.programState is None or self.graph is None:
            return None

        newProgramState = main.takeStep(self.image, self.programState)
        if isinstance(newProgramState, bool):
            return False

        self.programState = newProgramState
        self.selectedPosition = self.programState.position
        self.update()
        print("Take step!")
        return True


    def setBreakpoint(self):
        print("BREAKPOINT")


    def setExecutionSpeed(self, pos):
        if 0 < float(pos) < 100:
            self.executionSpeed = float(pos)

    def getWaitTime(self):
        return self.executionSpeed/100*self.maxWait

    def runProgram(self):
        if self.graph is None or self.image is None:
            return None

        step = self.takeStep()
        if step:
            timer = threading.Timer(self.getWaitTime(), self.runProgram)
            timer.start()
            return True
        else:
            return False


    def setScale(self):
        scaleValue = int(self.builder.get_object('scaleEntry', self.optionBar).get())
        if 0 < scaleValue < 100:
            self.scaleSize = int(scaleValue)
            self.update()
        print("SCALE")


    def loadFile(self):
        fileName = self.builder.get_object('fileNameEntry', self.optionBar).get()
        self.image = imageWrapper.getImage(fileName)
        self.graph = lexer.graphImage(self.image)
        self.programState = programState.programState(self.graph, (0,0), (0,0))

        self.update()
        print("LOAD FILE!")


    def canvasPressed(self, event):
        unscaled_x = int(event.x / self.scaleSize)
        unscaled_y = int(event.y / self.scaleSize)

        self.selectedPosition = (unscaled_x, unscaled_y)
        self.update()


if __name__ == '__main__':
    app = GUI()
    app.run()
