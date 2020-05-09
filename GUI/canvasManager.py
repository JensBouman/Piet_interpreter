import interpreter.imageFunctions as imageWrapper


class canvasManager():
    def __init__(self, canvas, image, programState, scaleSize):
        self.canvas = canvas
        self.image = image
        self.programState = programState
        self.previousProgramState = None
        self.scaleSize = scaleSize


    def updateImage(self, newImage):
        self.image = newImage


    def updateScaleSize(self, scaleSize):
        self.scaleSize = scaleSize


    def updateProgramState(self, newProgramState):
        self.previousProgramState = self.programState
        self.programState = newProgramState


    def pixelToHexString(self, pixel) -> str:
        """
        Transforms the color of a pixel to hex-string
        :param pixel: list with three values (RGB)
        :return:
        """
        return '#%02x%02x%02x' %(pixel[0], pixel[1], pixel[2])


    def updateCanvas(self):
        """
        Draws the canvas, then highlights the current codel. If a previous game state exists, it only reverses the highlight, instead of redrawing the entire canvas
        :return:
        """
        if self.image is None or self.canvas is None or self.programState is None or self.scaleSize is None:
            print("one is not none")
            return False

        if self.previousProgramState is None:
            self.drawImage()
        else:
            self.unHighlightCodel()
        self.highlightCodel()
        return True


    def drawImage(self):
        """
        Draw the image pixel for pixel, upscaled to the scaleSize.
        :return:
        """
        self.clearCanvas()
        for raw_y, row in enumerate(self.image):
            for raw_x, pixel in enumerate(row):
                x = raw_x * self.scaleSize
                y = raw_y * self.scaleSize
                color = self.pixelToHexString(pixel)
                self.canvas.create_rectangle(x,y, x+self.scaleSize, y+self.scaleSize, fill=color, outline=color)


    def clearCanvas(self):
        """
        Draws a white rectangle over the canvas
        :return:
        """
        width = len(self.image[0]) * self.scaleSize
        height = len(self.image) * self.scaleSize
        self.canvas.create_rectangle(0,0, width, height, fill="#FFFFFF")


    def highlightCodel(self):
        """
        Outlines the current codel with complemented colors
        :return:
        """
        codel = imageWrapper.getCodel(self.image, self.programState.position)
        pixel = imageWrapper.getPixel(self.image, self.programState.position)
        color = self.pixelToHexString(pixel)
        outline = self.pixelToHexString(self.complement(int(pixel[0]), int(pixel[1]), int(pixel[2])))
        self.colorCodel(codel, color, outline)


    def unHighlightCodel(self):
        codel = imageWrapper.getCodel(self.image, self.previousProgramState.position)
        pixel = imageWrapper.getPixel(self.image, self.previousProgramState.position)
        color = self.pixelToHexString(pixel)
        self.colorCodel(codel, color, color)


    def colorCodel(self, codel, fill, outline):
        for position in codel.codel:
            x = position.coords[0] * self.scaleSize
            y = position.coords[1] * self.scaleSize
            self.canvas.create_rectangle(x,y, x+self.scaleSize - 1, y+self.scaleSize - 1, fill=fill, outline=outline)


    def hilo(self, a, b, c):
        """
        Credit to StackOverflow user 'PM 2Ring' for making this code.
        """
        if c < b: b, c = c, b
        if b < a: a, b = b, a
        if c < b: b, c = c, b
        return a + c


    def complement(self, r, g, b):
        """
        Credit to StackOverflow user 'PM 2Ring' for making this code.
        """
        if r == 255 and g == 255 and b == 255:
            return (0,0,0)
        k = self.hilo(r, g, b)
        return tuple(k - u for u in (r, g, b))
