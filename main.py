import argparse
import sys

sys.setrecursionlimit(100000)

from interpreter import executeFunctions as executionFunctions
from interpreter import imageFunctions as imageWrapper
from GUI import main as GUIMain

parser = argparse.ArgumentParser(description='Interprets a piet image')
parser.add_argument("-f", "--file", required=True, type=str, help="complete filepath to a .png or .gif image")
parser.add_argument("-v", "--verbose", action="store_true", help="Outputs number of steps to STDOUT")
parser.add_argument("-g", "--graphical", action="store_true", help="Opens GUI with the file loaded")

args = parser.parse_args()

if not args.graphical:
    executionFunctions.interpret(imageWrapper.getImage(args.file))

    if args.verbose:
        print("\nTotal steps: {}".format(executionFunctions.takeStep.counter))
else:
    app = GUIMain.GUI()
    app.setFileText(args.file)
    app.loadFile()
    app.run()
