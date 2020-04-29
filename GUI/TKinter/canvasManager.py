import interpreter.imageWrapper as imageWrapper


class canvasManager():
    def __init__(self, canvas, image, programState, scaleSize):
        self.canvas = canvas
        self.image = image
        self.programState = programState
        self.scaleSize = scaleSize

    def updateImage(self, newImage):
        self.image = newImage

    def updateScaleSize(self, scaleSize):
        self.scaleSize = scaleSize

    def updateProgramState(self, newProgramState):
        self.programState = newProgramState

    def pixelToHexString(self, pixel) -> str:
        return '#%02x%02x%02x' %(pixel[0], pixel[1], pixel[2])

    def updateCanvas(self):
        if self.image is None or self.canvas is None or self.programState is None or self.scaleSize is None:
            return False
        self.drawImage()
        self.highlightCodel()
        # Draw breakpoint
        return True

    def drawImage(self):
        self.clearCanvas()
        for raw_y, row in enumerate(self.image):
            for raw_x, pixel in enumerate(row):
                x = raw_x * self.scaleSize
                y = raw_y * self.scaleSize
                color = self.pixelToHexString(pixel)
                self.canvas.create_rectangle(x,y, x+self.scaleSize, y+self.scaleSize, fill=color, outline=color)


    def clearCanvas(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.create_rectangle(0,0, width, height, fill="#FFFFFF")


    def highlightCodel(self):
        codel = imageWrapper.getCodel(self.image, self.programState.position)
        pixel = imageWrapper.getPixel(self.image, self.programState.position)
        color = self.pixelToHexString(pixel)
        self.colorCodel(codel, color, "#000000")

    def colorCodel(self, codel, fill, outline):
        for position in codel:
            x = position[0] * self.scaleSize
            y = position[1] * self.scaleSize
            self.canvas.create_rectangle(x,y, x+self.scaleSize - 1, y+self.scaleSize - 1, fill=fill, outline=outline)
