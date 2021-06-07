# importing libraries
from PySide2 import QtWidgets, QtGui, QtCore
import random
import sys

import res  # Import resources file

# creating game window


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # set window icon to image from resource file
        self.setWindowIcon(QtGui.QIcon(":/1/py_icon1.png"))
        self.board = Board(self)  # creating a board object
        self.statusbar = self.statusBar()  # creating a status bar to show result
        # adding border to the status bar
        self.statusbar.setStyleSheet("border : 2px solid black;")
        # calling showMessage method when signal received by board
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.setCentralWidget(self.board)  # adding board as a central widget
        self.setWindowTitle('Snake game')  # setting title to the window
        self.setGeometry(100, 100, 600, 400)  # setting geometry to the window
        self.board.start()  # starting the board object
        self.show()  # showing the main window


# creating a board class that inherits QFrame
class Board(QtWidgets.QFrame):
    msg2statusbar = QtCore.Signal(str)  # creating signal object
    SPEED = 80  # speed of the snake, timer countdown time
    WIDTHINBLOCKS = 60  # block width
    HEIGHTINBLOCKS = 40  # block height

    # constructor
    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QtCore.QBasicTimer()  # creating a timer
        self.snake = [[5, 10], [5, 11]]  # snake
        self.current_x_head = self.snake[0][0]  # current head x
        self.current_y_head = self.snake[0][1]  # current y head
        self.food = []  # food list
        self.grow_snake = False  # growing is false
        self.board = []  # board list
        self.direction = 1  # direction
        self.is_paused = False  # pause is false
        self.drop_food()  # called drop food method
        self.setFocusPolicy(QtGui.Qt.StrongFocus)  # setting focus

    # square width method
    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    # square height
    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    # start method
    def start(self):
        # msg for status bar, score = current len - 2
        self.msg2statusbar.emit('Score: ' + str(len(self.snake) - 2))
        self.timer.start(Board.SPEED, self)  # starting timer

    # paint event
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)  # creating painter object
        rect = self.contentsRect()  # getting rectangle
        # board top
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()
        # drawing snake
        for pos in self.snake:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
        # drawing food
        for pos in self.food:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

    # drawing square
    def draw_square(self, painter, x, y):
        color = QtGui.QColor(0x228B22)  # color
        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    # key press event
    def keyPressEvent(self, event):
        key = event.key()  # getting key pressed
        # prev_key = key  # store the previously pressed key
        # if left key pressed
        if not self.is_paused:
            if key == QtGui.Qt.Key_Left:
                # if direction is not right
                if self.direction != 2:
                    # set direction to left
                    self.direction = 1
            # if right key is pressed
            elif key == QtGui.Qt.Key_Right:
                # if direction is not left
                if self.direction != 1:
                    # set direction to right
                    self.direction = 2
            # if down key is pressed
            elif key == QtGui.Qt.Key_Down:
                # if direction is not up
                if self.direction != 4:
                    # set direction to down
                    self.direction = 3
            # if up key is pressed
            elif key == QtGui.Qt.Key_Up:
                # if direction is not down
                if self.direction != 3:
                    # set direction to up
                    self.direction = 4
            # if space bar is pressed
            elif key == QtGui.Qt.Key_Space:
                self.msg2statusbar.emit('Game Paused')
                self.is_paused = True
                self.timer.stop()
        # if paused and space bar is pressed
        elif key == QtGui.Qt.Key_Space:
            self.msg2statusbar.emit('Score: ' + str(len(self.snake)-2))
            self.is_paused = False
            self.timer.start(Board.SPEED, self)
            self.update()

    # method to move the snake

    def move_snake(self):
        # if direction is left change its position
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            # if it goes beyond left wall
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1
        # if direction is right change its position
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            # if it goes beyond right wall
            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
        # if direction is down change its position
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            # if it goes beyond down wall
            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
        # if direction is up change its position
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            # if it goes beyond up wall
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS
        # changing head position
        head = [self.current_x_head, self.current_y_head]
        # inset head in snake list
        self.snake.insert(0, head)
        # if snake grow is False
        if not self.grow_snake:
            # pop the last element
            self.snake.pop()
        else:
            # show msg in status bar
            self.msg2statusbar.emit('Score: ' + str(len(self.snake)-2))
            # make grow_snake to false
            self.grow_snake = False

    # time event method
    def timerEvent(self, event):
        # checking timer id
        if event.timerId() == self.timer.timerId():
            # call move snake method
            self.move_snake()
            # call food collision method
            self.is_food_collision()
            # call is suicide method
            self.is_suicide()
            # update the window
            self.update()

    # method to check if snake collides itself
    def is_suicide(self):
        # traversing the snake
        for i in range(1, len(self.snake)):
            # if collision found
            if self.snake[i] == self.snake[0]:
                # show game ended msg in status bar
                self.msg2statusbar.emit(
                    str("Game Ended-" + "Your Score: " + str(len(self.snake)-2)))
                # making background color black
                self.setStyleSheet("background-color : black;")
                # stopping the timer
                self.timer.stop()
                # updating the window
                self.update()

    # method to check if the food cis collied
    def is_food_collision(self):
        # traversing the position of the food
        for pos in self.food:
            # if food position is similar of snake position
            if pos == self.snake[0]:
                # remove the food
                self.food.remove(pos)
                # call drop food method
                self.drop_food()
                # grow the snake
                self.grow_snake = True

    # method to drop food on screen
    def drop_food(self):
        # creating random co-ordinates
        x = random.randint(3, 58)
        y = random.randint(3, 38)
        # traversing if snake position is not equal to the
        # food position so that food do not drop on snake
        for pos in self.snake:
            # if position matches
            if pos == [x, y]:
                # call drop food method again
                self.drop_food()
        # append food location
        self.food.append([x, y])


# main method
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Window()
    sys.exit(app.exec_())
