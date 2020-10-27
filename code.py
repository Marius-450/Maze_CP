import board
import busio
import time
import math
from random import randint
from adafruit_gizmo import tft_gizmo
import adafruit_lis3dh


import adafruit_imageload

import displayio
import digitalio


# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()



# shake sensitivity, lower=more sensitive
SHAKE_THRESHOLD = 25

# Accelerometer setup
accelo_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelo = adafruit_lis3dh.LIS3DH_I2C(accelo_i2c, address=0x19)


# functions

def get_angle():
    x, y, z = accelo.acceleration
    angle = math.degrees(math.atan2(y,x)) + 90.0
    if angle < 0:
        angle = 360 + angle
    #print(angle, abs(z))
    return (angle, abs(z))

def collision(a, b):
    # ~6.5 pixels distance minimum for collision (6.5^2 = 42.25)
    if abs(a.x-b.x)**2 + abs(a.y-b.y)**2 < 43:
        # collision
        # print("COLLISION !!!")
        return True
    else:
        return False

def shuffle(x):
    """Shuffle list x in place, and return None.
    From Cpython source code
    """
    for i in reversed(range(1, len(x))):
        # pick an element in x[:i+1] with which to exchange x[i]
        j = randint(0,i)
        x[i], x[j] = x[j], x[i]
#


def reinit_maze(x, y):

    for i in range(0,8):
        for j in range(0,8):
            maze[i,j] = 1
            time.sleep(0.01)

    goal_group.hidden = True

    start_pos, goal_pos = generate_maze(start_x=x, start_y=y)
    goal_tilegrid.x = goal_pos[0]*29 + 13
    goal_tilegrid.y = goal_pos[1]*29 + 13
    goal_group.hidden = False


    return True

def generate_maze(start_x=None, start_y=None):
    global max_depth, goal_x, goal_y
    w = 8
    h = 8
    max_depth = 0
    goal_x = 0
    goal_y = 0
    # visited cells
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    path = []

    def walk(x, y, depth):
        global max_depth, goal_x, goal_y
        path.append((x,y))
        while len(path)>0:
            move = False
            if depth > max_depth:
                max_depth = depth
                goal_x = x
                goal_y = y
            if vis[y][x] != 1 :
                path.append((x,y))
                vis[y][x] = 1
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if xx > 7 or yy > 7: continue
                if vis[yy][xx]: continue
                move = True
                if xx == x:
                    # vertical move
                    if yy > y:
                        # going south
                        maze[x,yy] = 3
                    else:
                        # going north
                        if maze[x,y] == 1:
                            maze[x,y] = 3
                        else:
                            maze[x,y] = 2
                if yy == y:
                    # horizontal move
                    if xx > x:
                        # going east
                        if maze[x,y] == 1:
                            maze[x,y] = 0
                        else:
                            maze[x,y] = 2
                    else:
                        #going west
                        maze[xx,y] = 0
                if move:
                    print("moving to", xx, yy)
                    x,y,depth = (xx, yy, depth + 1)
                    time.sleep(0.05)
                    break

            if move:
                continue
            else:
                path.pop()
                if len(path) < 1:
                    print("maze completed")
                    break
                x,y = path[-1]
                depth -= 1
                print("moving back to", x, y)

    if start_x == None:
        start_x = randint(0,7)

    if start_y == None:
        start_y = randint(0,7)
    start = (start_x, start_y)
    walk(start_x, start_y, 1)
    goal = (goal_x, goal_y)
    print(start, goal, max_depth)
    return start, goal



# init buttons :
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.DOWN

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.DOWN

# state variables

# buttons
but_a = False
but_b = False


# graphical init

# Maze
maze_sprite_sheet, maze_palette = adafruit_imageload.load("/Maze_tiles2.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

maze = displayio.TileGrid(maze_sprite_sheet, pixel_shader=maze_palette,
                            width = 8,
                            height = 8,
                            tile_width = 29,
                            tile_height = 29,
                            default_tile = 1)

maze_group = displayio.Group()
maze_group.append(maze)
maze_group.x = 8

# Walls

wallH_sprite_sheet, wallH_palette = adafruit_imageload.load("/Walltile_H.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

wall_H = displayio.TileGrid(wallH_sprite_sheet, pixel_shader=wallH_palette,
                            width = 9,
                            height = 1,
                            tile_width = 29,
                            tile_height = 8 )

wall_H_group = displayio.Group()
wall_H_group.append(wall_H)
wall_H_group.y = 232

wallV_sprite_sheet, wallV_palette = adafruit_imageload.load("/Walltile_V.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

wall_V = displayio.TileGrid(wallV_sprite_sheet, pixel_shader=wallV_palette,
                            width = 1,
                            height = 9,
                            tile_width = 8,
                            tile_height = 29 )

wall_V_group = displayio.Group()
wall_V_group.append(wall_V)

# Sprites

# Ball

ball_sprite_sheet, ball_palette = adafruit_imageload.load("/Billiard_Balls_01_Red_10x10.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

ball = displayio.TileGrid(ball_sprite_sheet, pixel_shader=ball_palette,
                            width = 1,
                            height = 1,
                            tile_width = 10,
                            tile_height = 10 )

ball_group = displayio.Group()
ball_group.append(ball)

# debug to find wich color is white
#a = 0
#for color in ball_palette:
#    print(a, hex(color))
#    a += 1
ball_palette.make_transparent(54)
ball_group.hidden = True

# Goal

goal_sprite_sheet, goal_palette = adafruit_imageload.load("/goal.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

goal_tilegrid = displayio.TileGrid(goal_sprite_sheet, pixel_shader=goal_palette,
                            width = 1,
                            height = 1,
                            tile_width = 10,
                            tile_height = 10 )

goal_group = displayio.Group()
goal_group.append(goal_tilegrid)

# debug to find wich color is white
#a = 0
#for color in goal_palette:
#    print(a, hex(color))
#    a += 1
goal_palette.make_transparent(1)
goal_group.hidden = True


# Create a Group to hold the sprites and maze
group = displayio.Group(max_size=6)

group.append(maze_group)
group.append(wall_H_group)
group.append(wall_V_group)
group.append(ball_group)
group.append(goal_group)

#Show the group (walls everywhere)

display.show(group)

print("Maze time! Find the exit...")

# generating the maze, returning two tupples : start and exit tiles coordinates
start_position, goal_position = generate_maze()

# Start position for the ball

ball.x = start_position[0]*29 + 13
ball.y = start_position[1]*29 + 13
ball_group.hidden = False

# Goal position

goal_tilegrid.x = goal_position[0]*29 + 13
goal_tilegrid.y = goal_position[1]*29 + 14
goal_group.hidden = False

while True:
    # accelerometer values
    angle, z = get_angle()
    grid_x = []
    grid_y = []

    if (ball.x-8)// 29 == (ball.x+2)// 29:
        grid_x = [(ball.x-8)// 29]
    else:
        grid_x = [(ball.x-8)// 29, (ball.x+2)// 29]
    if ball.y // 29 == (ball.y+10) // 29:
        grid_y = [ball.y // 29]
    else:
        grid_y = [ball.y // 29, (ball.y+10) // 29]

    # Ball collision with goal.
    if collision(ball, goal_tilegrid):
        reinit_maze(grid_x[0], grid_y[0])
        pass


    # moving the ball

    # Set speed relative to tilt
    if z > 9.67:
        # print ("do nothing, z =", z)
        delta_x = 0
        delta_y = 0
    else:
        if z > 9:
            speed = 1
        elif z > 6:
            speed = 3
        elif z > 4:
            speed = 4
        else:
            speed = 5
        delta_x = (3 + speed) * math.sin(math.radians(angle))
        delta_y = (-3 - speed) * math.cos(math.radians(angle))

    # collision detection with walls

    # distances = [N, E, S, W] in pixels
    distances = [0,0,0,0]
    # relative position of the ball in the cell
    local_x = ball.x - 8 - grid_x[0]*29
    local_y = ball.y - grid_y[0]*29
    # North distance
    if maze[grid_x[0],grid_y[0]] < 2:
        distances[0] = local_y - 8
    else:
        if maze[grid_x[0],grid_y[0]] == 2:
            if local_x > 11:
                distances[0] = local_y - 8
            else:
                distances[0] = 40
        else:
            distances[0] = 40
    # East distance
    if maze[grid_x[0],grid_y[0]] % 2 == 1:
        distances[1] =  29 - local_x - 18
    else:
        if maze[grid_x[0],grid_y[0]] == 2:
            if local_y < 8:
                distances[1] =  29 - local_x - 8
            else:
                distances[1] = 40
        else:
            distances[1] = 40

    # South distance
    if grid_y[0] < 7:
        if local_x > 11:
            distances[2] = 19 - local_y
        else:
            if  maze[grid_x[0],grid_y[0]+1] < 2:
                distances[2] = 19 - local_y
            else :
                distances[2] = 40
    else:
        distances[2] = 19 - local_y
    # West distance
    if grid_x[0] > 0:
        if local_y < 8:
            distances[3] = local_x
        else:
            if maze[grid_x[0]-1,grid_y[0]] % 2 == 1:
                distances[3] = local_x
            else:
                distances[3] = 40
    else:
        distances[3] = local_x

    # if planned move is greater than available space, replace delta by distances[]
    if math.ceil(delta_x) > distances[1]:
        delta_x = distances[1]
    if math.ceil(delta_x) < -distances[3]:
        delta_x = -distances[3]
    if math.ceil(delta_y) > distances[2]:
        delta_y = distances[2]
    if math.ceil(delta_y) < -distances[0]:
        delta_y = -distances[0]

    ball.x += math.ceil(delta_x)
    ball.y += math.ceil(delta_y)

    # actions for pressing or releasing buttons
    # unused now

    if button_a.value and but_a == False:
        print("Button A pressed")
        a_presstime = time.monotonic()
        but_a = True

    if but_a and button_a.value == False:
        if time.monotonic() - a_presstime > 2.0:
            print("Button A released from long press")
        else:
            print("Button A released")
        but_a = False

    #Button B

    if button_b.value and but_b == False:
        print("Button B pressed")
        b_presstime = time.monotonic()
        but_b = True

    if but_b and button_b.value == False:
        # print("button b released")
        if time.monotonic() - b_presstime > 2.0:
            # long press released
            print("Button B released from long press")
        else:
            # short press released
            print("Button B released")
        but_b = False
    #if accelo.shake(SHAKE_THRESHOLD, 6, 0.04):
        # TODO : reaction ?

    time.sleep(0.04)
