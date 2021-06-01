import random
import curses

s = curses.initscr()  # initialize the screen
curses.curs_set(0)  # set the cursor to zero, so that it does not show up on screen # nopep8
sh, sw = s.getmaxyx()  # get the height and the width
w = curses.newwin(sh, sw, 0, 0)  # create a new window from the height and width, and start it at the top left corner of screen # nopep8
w.keypad(1)  # accept keypad input
w.timeout(100)  # refresh the screen every 100 milliseconds

# Create snakes initial position
snk_x = int(sw/4)  # the 'x' will be the width of screen divided by four
snk_y = int(sh/2)  # the 'y' will be the height of screen divided by two

# Create snake body part
snake = [
    [snk_y, snk_x],
    [snk_y, int(snk_x-1)],  # one left of the head
    [snk_y, int(snk_x-2)]  # two left of the head
]

# Create the food
# the starting place of the food is the center of the screen
food = [int(sh/2), int(sw/2)]
w.addch(food[0], food[1], curses.ACS_PI)  # add food to the screen

# Set the score to zero and add it to the bottom left of the screen
score = 0
w.addstr(int(sh-1), 0, f"Score:{score}")

# Message that will be displayed at the end of game
end_msg = 'Game Over'
half_len_msg = int(len(end_msg)/2)

# tell snake where to go initially
key = curses.KEY_RIGHT

# infinite loop for every movement of the snake
while True:
    next_key = w.getch()  # see what the next key is
    key = key if next_key == -1 else next_key

    # check if person has lost the game
    """ you will lose if:
               1) the y position is at the top/height of screen or
               2) the x position is to the left/width of screen or
               3) the   position is at the bottom of screen or
               4) the   position is at the right of screen or
               5) your snake is in itself    """
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0][0] in [0, sh-1] or snake[0][1] in [0, sw-1] or snake[0] in snake[1:]:
        w.clear()  # Clear the screen
        # Display 'Game Over' in center screen
        w.addstr(int(sh/2), int(int(sw/2) - half_len_msg), end_msg)
        w.refresh()
        curses.napms(3000)
        curses.endwin()  # kill window
        quit()

    # determine what the new head of snake will be, start with the old head of the snake
    new_head = [snake[0][0], snake[0][1]]

    # figure out which key is being pressed and move accordingly
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # insert the new head of snake
    snake.insert(0, new_head)

    # determine if snake has ran into the food
    if snake[0] == food:
        food = None
        score += 1  # add one point to the score
        w.addstr(int(sh-1), 0, f"Score:{score}")
        while food is None:
            # select new piece of food
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        # add a space to the where the tail piece was
        w.addch(tail[0], tail[1], ' ')

    # add the head of the snake to the screen
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
