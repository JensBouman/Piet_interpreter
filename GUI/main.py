import pygubu
import os

from interpreter import imageFunctions as imageWrapper
from interpreter import lexer as lexer
from interpreter import executeFunctions as main
from interpreter.dataStructures import programState, direction, position

from GUI import infoManager
from GUI import canvasManager


class GUI:
    def __init__(self):
        # In pixelWidth/height per pixel. scaleSize = 25 means that every pixel will show as a 25x25 square
        self.scaleSize = 15
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
        self.builder = pygubu.Builder()

        #2: Load an ui file
        self.builder.add_from_file("{}/tkinterLayout.ui".format(os.path.abspath(os.path.dirname(__file__))))

        #3: Create the mainwindow
        self.mainwindow = self.builder.get_object('rootWindow')

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
            'takeStep': self.takeStep
        })

        horizontalBar = self.builder.get_object("canvasHorizontalScroll", self.canvasFrame)
        verticalBar = self.builder.get_object("canvasVerticalScroll", self.canvasFrame)
        horizontalBar.config(command = self.canvas.xview)
        verticalBar.config(command = self.canvas.yview)
        self.canvas.config(xscrollcommand=horizontalBar.set, yscrollcommand=verticalBar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def initializeFrames(self):
        self.optionBar = self.builder.get_object('optionBar', self.mainwindow)
        self.content = self.builder.get_object('content', self.mainwindow)
        self.actionBar = self.builder.get_object('actionBar', self.mainwindow)
        self.generalInfoFrame = self.builder.get_object("generalInfoFrame", self.content)
        self.programStateInfoFrame = self.builder.get_object("programStateInfoFrame", self.content)
        self.canvasFrame = self.builder.get_object('canvasFrame', self.content)
        self.canvas = self.builder.get_object('canvas', self.canvasFrame)


    def update(self):
        self.infoManager.updateInfo(self.image, self.graph, self.programState)
        self.canvasManager.updateScaleSize(self.scaleSize)
        self.canvasManager.updateImage(self.image)
        self.canvasManager.updateProgramState(self.programState)
        self.canvasManager.updateCanvas()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def takeStep(self):
        if self.image is None or self.programState is None or self.graph is None:
            return None

        newProgramState = main.takeStep(self.image, self.programState)
        # Error encountered, close window
        if isinstance(newProgramState, BaseException):
            self.mainwindow.destroy()
            self.mainwindow.quit()
            raise newProgramState

        self.programState = newProgramState
        self.selectedPosition = self.programState.position
        self.update()
        return True


    def setFileText(self, filePath):
        self.builder.get_object("fileNameEntry", self.optionBar).delete(0, len(self.builder.get_object("fileNameEntry", self.optionBar).get()))
        self.builder.get_object("fileNameEntry", self.optionBar).insert(0, filePath)


    def setExecutionSpeed(self, pos):
        if 0 < float(pos) < 100:
            self.executionSpeed = float(pos)


    def setScale(self):
        scaleValue = int(self.builder.get_object('scaleEntry', self.optionBar).get())
        if 0 < scaleValue < 100:
            self.canvasManager.clearCanvas()
            self.scaleSize = int(scaleValue)
            self.update()
            self.canvasManager.drawImage()
            self.canvasManager.updateCanvas()


    def loadFile(self):
        fileName = self.builder.get_object('fileNameEntry', self.optionBar).get()
        if len(fileName) < 1:
            return None
        try:
            tmpImage = imageWrapper.getImage(fileName)
        except FileNotFoundError:
            edgeInfo = self.infoManager.builder.get_object('codelEdgesMessage', self.infoManager.generalInfo)
            edgeInfo.configure(text="The file '{}' could not be found".format(fileName))
            return False

        tmpResult = lexer.graphImage(tmpImage)
        if len(tmpResult[1]) != 0:
            edgeInfo = self.infoManager.builder.get_object('codelEdgesMessage', self.infoManager.generalInfo)
            edgeInfo.configure(text="The following exceptions occured while making the graph:\n{}".format("".join(list(map(lambda x: "\t{}\n".format(x), tmpResult[1])))))
            return False

        self.image = tmpImage
        self.graph = tmpResult[0]
        self.programState = programState(self.graph, position((0,0)), direction((0,0)))
        # Reset previous state
        self.canvasManager.previousProgramState = None
        self.canvasManager.programState = None
        self.update()
