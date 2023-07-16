import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from UI.animation_creator_ui import Ui_animation_creator
from Widgets.canvas import Canvas


class AnimationCreator(QtWidgets.QMainWindow, Ui_animation_creator):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        '''
            Sets up a new canvas widget by calling Canvas()
            Adds the canvas to the drawing_area which is a QVBoxLayout
            Initialises an individual color dialog window to use in the color picker and background picker
        '''
        self.canvas = Canvas()
        self.drawing_area.addWidget(self.canvas)
        self.color_dialog_pen = QtWidgets.QColorDialog(self)
        self.color_dialog_background = QtWidgets.QColorDialog(self)

        '''
            Calls the set_brush_size method and sets it to the value of the brushSize slider, when the value of the slider is changed
            lambda is used to create an anonymous function, : separates it from the expression
            It allows us to pass the value of the slider into the set_brush_size(size) as it is expecting an arguement
            If this isn't there then the valueChanged will emit a signal and pass it directly to set_brush_size not it's size arguement
        '''
        self.h_slider_brushSize.valueChanged.connect(lambda: self.canvas.set_brush_size(self.h_slider_brushSize.value()))

        # Install an event filter on the color pickers to handle mouse enter events
        self.color_picker.installEventFilter(self)
        self.background_picker.installEventFilter(self)

        '''
            Initialises two variables to store the current color and the previous color
            On startup it will define the current color as red which is what the pb_color_button is
            The old color will be left blank
            Initialises a background color variable to be used with the eraser
        '''
        self.bt_color_current = '#ff0000'
        self.bt_color_old = ''
        self.background_color = '#ffffff'

        # Methods to quickly change colors or to eraser by pressing the push buttons
        self.pb_black_button.pressed.connect(self.black_button)
        self.pb_white_button.pressed.connect(self.white_button)
        self.pb_color_button.pressed.connect(self.color_button)
        self.pb_eraser.pressed.connect(self.eraser_button)

    '''
        If the mouse enters the color_picker or bg picker it will show the color GUI
        It looks to see if the mouse is over the picker, and if the event is a mouseover
    '''
    def eventFilter(self, obj, event):
        if obj == self.color_picker and event.type() == QtCore.QEvent.Enter:
            self.show_color_picker()

        if obj == self.background_picker and event.type() == QtCore.QEvent.Enter:
            self.show_background_picker()

        # Passes the event handling to the parent class (AnimationCreator) to ensure that other events can still occur if necessary
        return super().eventFilter(obj, event)

    '''
        When the current color of the widget is changed we call the color_changed method
        QColorDialog.Accepted is a constant that has a value of 1
        If color_dialog is exited it's value set to 1
        This basically checks if the user has selected a color and clicked ok
        We don't need anything to happen so we pass
    '''
    def show_color_picker(self):

        self.color_dialog_pen.currentColorChanged.connect(self.color_changed)

        if self.color_dialog_pen.exec_() == QtWidgets.QColorDialog.Accepted:
            pass
    
    # See show_color_picker notes
    def show_background_picker(self):

        self.color_dialog_background.currentColorChanged.connect(self.background_color_changed)

        if self.color_dialog_background.exec_() == QtWidgets.QColorDialog.Accepted:
            pass

    '''
        If the  selected color is a valid color
        The background color of the label is set to the selected color
        Border-radius is applied to keep the round shape
        The pen color is set to the color we just selected by calling the set_pen_color method
        The color text is changed to be the current color
    '''
    def color_changed(self, color):    
        if color.isValid():
            color_picker_style = f'background-color:{color.name()}; border-radius:65%; border: 1px solid black;'
            self.color_picker.setStyleSheet(color_picker_style)
            self.canvas.set_pen_color(color.name())
            self.color_name_text.setText(f'{color.name()}')

            '''
                This stores the previously selected color
                It compares the current color variable to the new color
                If they are not the same then the old color gets updated to what what was current color
                The current color variable is then updated to be the new color
                The color_button changes to the old color
            '''
            if self.bt_color_current != color.name():
                self.bt_color_old = self.bt_color_current
            
            self.bt_color_current = color.name()
            self.pb_color_button.setStyleSheet( f'background-color:{self.bt_color_old};')

    '''
        If the selected color is a valid color
        background_color variable is set to the color (for use with eraser)
        The background color of the label is set to the selected color, border is applied
        The canvas color is set to the color we just selected by calling the set_bg_color method
        The bg color text is changed to be the current bg color
    '''
    def background_color_changed(self, color):
        if color.isValid():
            self.background_color = color
            self.background_picker.setStyleSheet(f'background-color:{color.name()}; border: 1px solid black;')
            self.canvas.set_bg_color(color.name())
            self.bg_color_text.setText(color.name())

    '''
        Sets the old color variable to the previously selected color
        Changes the color button style to the previously selected color
        Sets the color picker, pen, and color text to black
    '''
    def black_button(self):
        self.bt_color_old = self.bt_color_current
        self.pb_color_button.setStyleSheet( f'background-color:{self.bt_color_old};')
        self.color_picker.setStyleSheet( f'background-color:#000000; border-radius:65%; border: 1px solid black;')
        self.canvas.set_pen_color('#000000')
        self.color_name_text.setText('#000000')

    '''
        Sets the old color variable to the previously selected color
        Changes the color button style to the previously selected color
        Sets the color picker, pen, and color text to white
    '''
    def white_button(self):
        self.color_picker.setStyleSheet( f'background-color:#ffffff; border-radius:65%; border: 1px solid black;')
        self.canvas.set_pen_color('#ffffff')
        self.color_name_text.setText('#ffffff')

    '''
        The if statement is setting everything to the current color variable (red) if no color has been selected from the color picker yet
        Sets the color picker, pen, and color text to current color variable
        Sets the old color variable to the previously current color variable

        If a color has been selected then it will set the color picker, pen and color text to be the old color
    '''
    def color_button(self):
        if self.bt_color_old == '':
            self.color_picker.setStyleSheet(f'background-color:{self.bt_color_current}; border-radius:65%; border: 1px solid black;')
            self.canvas.set_pen_color(self.bt_color_current)
            self.color_name_text.setText(self.bt_color_current)
            self.bt_color_old = self.bt_color_current
        else:
            self.color_picker.setStyleSheet(f'background-color:{self.bt_color_old}; border-radius:65%; border: 1px solid black;')
            self.canvas.set_pen_color(self.bt_color_old)
            self.color_name_text.setText(self.bt_color_old)

    '''
        Pressing the eraser sets the pen color to the background color
        It sets the text of the color to Eraser
    '''
    def eraser_button(self):
        self.canvas.set_pen_color(self.background_color)
        self.color_name_text.setText('Eraser')

# creates an instance of QApplication and executes the program
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = AnimationCreator()
    window.show()

    # terminates the program if it is exited
    sys.exit(app.exec())