from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.properties import ObjectProperty

import interpreter.lexer as lexer
import interpreter.imageWrapper as imageWrapper


class GeneralLayout(GridLayout):
    pass

class ContentLayout(GridLayout):
    pass

class ImageCanvas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        image = None


    def drawImage(self, image, scale):
        app = App.get_running_app()
        self.image = app.loadImage(image)
        max_height = self.size
        print(max_height)
        with self.canvas:
            for y_axis, row in enumerate(image):
                for x_axis, pixel in enumerate(row):
                    x = x_axis*scale
                    y = y_axis*scale

                # with self.:
                #     Color([x/255 for x in pixel])
                #     Line(points = [x_axis, x, y_axis, y])


class OptionBar(BoxLayout):
    def setFile(self, value):
        app = App.get_running_app()
        app.loadImage(value)
        self.ids["filePath"].hint_text = value
        self.ids['filePath'].text = ""

    def setScale(self, value):
        app = App.get_running_app()
        self.ids['scaleSize'].hint_text = value
        self.ids['scaleSize'].text = ""
        app.pixelScale = value

class ToolBar(BoxLayout):
    pass


class DebuggerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pixelScale = 10
        self.canvas = ObjectProperty()


    def loadImage(self, filepath):
        image = imageWrapper.getImage(filepath)
        return image

    def build(self):
        return GeneralLayout()

if __name__ == '__main__':
    GUI = DebuggerApp()
    GUI.run()
