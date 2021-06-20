### tetris ###

class oblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = oblock

    def forms(self):
        return [[[0,0], [0,-1], [1,-1], [1,0]]]

    def unders(self):
        return [[[0, 1], [1, 1]]]

class lblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = lblock

    def forms(self):
        return [[[0,0],[-1,0], [-2,0], [0,-1]], [[0,0],[0,-1], [0,-2], [1,0]], [[0,0],[0,1], [1,0], [2,0]], [[0,0],[-1,0], [0,1], [0,2]]]

    def unders(self):
        return [[[0,1],[-1,1],[-2,1]],[[0,1],[1,1]],[[0,2],[1,1],[2,1]],[[0,3],[-1, 1]]]

class jblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = jblock

    def forms(self):
        return [[[0,0],[1,0], [2,0], [0,-1]], [[0,0],[0,1], [0,2], [1,0]], [[0,0],[0,1], [-1,0], [-2,0]], [[0,0],[-1,0], [0,-1], [0,-2]]]

    def unders(self):
        return [[[0,1],[1,1],[2,1]],[[0,3],[1,1]],[[0,2],[-1,1],[-2,1]],[[0,1],[-1, 1]]]

class iblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = iblock

    def forms(self):
        return [[[0,0], [0, -1], [0, 1], [0, 2]], [[0,0], [1, 0], [-1, 0], [-2, 0]]]

    def unders(self):
        return [[[0, 3]], [[0,1], [1, 1], [-1, 1], [-2, 1]]]

class sblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = sblock

    def forms(self):
        return [[[0,0], [0, -1], [1, -1], [-1, 0]], [[0, 0], [0, -1], [1, 0], [1,1]]]

    def unders(self):
        return [[[1, 0], [0, 1], [-1, 1]], [[0, 1], [1, 2]]]

class zblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = zblock

    def forms(self):
        return [[[0,0], [0, -1], [-1, -1], [1, 0]], [[0, 0], [0, -1], [-1, 0], [-1,1]]]

    def unders(self):
        return [[[-1, 0], [0, 1], [1, 1]], [[0, 1], [-1, 2]]]

class tblock:
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.blocktype = tblock

    def forms(self):
        return [[[0,0], [1, 0], [-1, 0], [0, -1]], [[0,0], [1, 0], [0, -1], [0, 1]], [[0,0], [1, 0], [-1, 0], [0, 1]], [[0,0], [-1, 0], [0, -1], [0, 1]]]

    def unders(self):
        return [[[0,1], [1, 1], [-1, 1]], [[0, 2], [1, 1]], [[0, 2], [1, 1], [-1, 1]], [[0, 2], [-1, 1]]]

import random

def randomblocktype():
    n = random.randint(0,6)
    return [oblock, lblock, jblock, iblock, sblock, tblock, zblock][n]

def breakline(board):
    for i in range(4):
        for a in range(len(board)-1, 0, -1):
            if board[a]==["x", "x", "x", "x", "x", "x", "x", "x", "x", "x"]:
                for a in range(a, 0, -1):
                    board[a]=board[a-1]
                board[0]= [" "," "," "," "," "," "," "," "," "," "]

def spawn(blocktype, board, x, y, form):
    o = blocktype(x, y, form)
    for a in o.forms()[o.form]:
        if board[o.y+a[1]][o.x + a[0]] == "x":
            print("game over")
            print_board(board)
            quit()
        board[o.y+a[1]][o.x + a[0]] = "o"

    for a in o.unders()[o.form]:
        if o.y+a[1]>len(board)-1 or board[o.y+a[1]][o.x + a[0]] == "x":
            for b in o.forms()[o.form]:
                board[o.y+b[1]][o.x + b[0]] = "x"
            breakline(board)
            return spawn(randomblocktype(), board, 5, 1, 0)
    return o

def despawn(board, o):
    for a in o.forms()[o.form]:
        board[o.y+a[1]][o.x + a[0]] = " "

def move_right(board, o):
    for a in o.forms()[o.form]:
        if o.x + a[0] > 8:
            break
        elif board[o.y+a[1]][o.x + a[0]+1] == "x":
            break
    else:
        despawn(board, o)
        return spawn(o.blocktype, board, o.x+1, o.y, o.form)
    return o

def move_left(board, o):
    for a in o.forms()[o.form]:
        if o.x + a[0] < 1:
            break
        elif board[o.y+a[1]][o.x + a[0]-1] == "x":
            break
        elif board[o.y+a[1]][o.x + a[0]-2] == "x":
            break
    else:
        despawn(board, o)
        return spawn(o.blocktype, board, o.x-1, o.y, o.form)
    return o

def move_down(board, o):
    despawn(board, o)
    return spawn(o.blocktype, board, o.x, o.y+1, o.form)

def rotate(board, o):
    for a in o.forms()[(o.form+1)%(len(o.forms()))]:
        if o.y+a[1] > len(board)-1 or o.x+a[0] > 9 or o.x+a[0] < 0:
            break
        if board[o.y+a[1]][o.x + a[0]] == "x":
            break
    else:
        despawn(board, o)
        return spawn(o.blocktype, board, o.x, o.y, (o.form+1)%(len(o.forms())))
    return o

def make_empty_board(height):
    board = []
    for i in range(height):
        board.append([" "]*10)
    return board

def print_board(board):
    s=""
    for i in range(len(board)):
        s += " "
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][9]) + "|\n"
    s += (len(board[0]) + 1) * "* "
    print(s)

import keyboard
import time

def play(height):
    global next_move
    next_move = ""
    board = make_empty_board(height)
    seconds = time.time()
    difficulty=2
    end = False
    counter = 0
    print_board(board)
    o=spawn(iblock, board, 5, 1, 0)
    while not end:
        if keyboard.is_pressed("a"):
            next_move= "a"
        if keyboard.is_pressed("d"):
            next_move= "d"
        if keyboard.is_pressed("r"):
            next_move= "r"
        if difficulty == 0:
            print ("cheater")
            return 0
        if seconds+difficulty < time.time():
            print_board(board)
            seconds = time.time()
            counter+= 1
            if next_move== "a":
                o = move_left(board, o)
                next_move=""
            if next_move== "d":
                o=move_right(board, o)
                next_move=""
            if next_move== "r":
                o=rotate(board, o)
                next_move=""
            o=move_down(board, o)
        if counter == 20:
            difficulty -= 0.1
            counter = 0
        time.sleep(0.04)
        
        

if __name__ == "__main__":
    play(18)
