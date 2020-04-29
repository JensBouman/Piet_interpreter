import interpreter.imageWrapper as imageWrapper
import interpreter.colors as colors
import interpreter.lexerTokens as lexerTokens
import interpreter.movement as movement

class infoManager():
    def __init__(self, builder, generalInfoFrame, programStateInfoFrame):
        self.builder = builder
        self.generalInfo = generalInfoFrame
        self.programStateInfoFrame = programStateInfoFrame

    def updateInfo(self, image, graph, programState):
        self.updateGeneralinfo(image, graph, programState)
        self.updateProgramStateInfo(programState)

    def updateGeneralinfo(self, image, graph, programState):
        self.updateCodelInfo(image, programState.position)
        self.updateEdgesInfo(image, graph, programState)

    def updateProgramStateInfo(self, programState):
        self.updateStackInfo(programState.dataStack)
        self.updatePointersInfo(programState.position, programState.pointers)

    def updateCodelInfo(self, image, newPosition):
        infoMessage = self.builder.get_object('positionInfoMessage', self.generalInfo)
        if colors.isBlack(imageWrapper.getPixel(image, newPosition)):
            infoMessage.configure(text="Black pixels are no codel, and have no edges")
            return None

        baseString = "Selected codel contains:\n"
        codel = imageWrapper.getCodel(image, newPosition)
        for position in codel:
            baseString += "{}\n".format(position)

        infoMessage.configure(text=baseString.strip('\n'))


    def updateEdgesInfo(self, image, graph, programState):
        edgesInfo = self.builder.get_object('codelEdgesMessage', self.generalInfo)

        if colors.isBlack(imageWrapper.getPixel(image, programState.position)):
            edgesInfo.configure(text = "Black pixels are no codel, and have no edges")
            return None

        codel = imageWrapper.getCodel(image, programState.position)
        baseString = "Next step will be:\n"
        edge = graph[hash(frozenset(codel))][hash(programState.pointers)]
        baseString += self.getEdgeDescription(edge, programState.pointers)

        baseString += "\nCodel edges are as follows:\n"
        #Generate pointers
        edgePointers = list(map(lambda i: (i%4, int(i/4)), iter(range(8))))
        for edgePointer in edgePointers:
            edge = graph[hash(frozenset(codel))][hash(edgePointer)]
            baseString += self.getEdgeDescription(edge, edgePointer)
        edgesInfo.configure(text = baseString)

    def getEdgeDescription(self, edge, pointer):
        if isinstance(edge[0], lexerTokens.toColorToken) and edge[0].type == "push":
            return "{}/{},{} -> {}({})\n".format(edge[1], movement.getDP(pointer[0]), movement.getCC(pointer[1]), edge[0].type, edge[0].codelSize)
        else:
            return "{}/{},{} -> {}\n".format(edge[1], movement.getDP(pointer[0]), movement.getCC(pointer[1]), edge[0].type)

    def updateStackInfo(self, stack):
        baseString = ""
        for item in reversed(stack):
            baseString += "{}\n".format(item)
        baseString.strip("\n")

        stackInfoMessage = self.builder.get_object("stackContents", self.programStateInfoFrame)
        stackInfoMessage.configure(text=baseString)

    def updatePointersInfo(self, position, pointers):
        print("Update pointers: {} -> Arrow: {}".format(pointers, movement.getArrow(pointers)))
        baseString = "Pos: ({},{})\n".format(position[0], position[1])
        baseString += u"DP: {} ({},{})".format(movement.getArrow(pointers), movement.getDP(pointers[0]), movement.getCC(pointers[1]))

        pointersInfoMessage = self.builder.get_object("pointerMessage", self.programStateInfoFrame)
        pointersInfoMessage.configure(text=baseString)
