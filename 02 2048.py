import curses
from random import randrange, choice
from coloections import defaultdict

actions = ["Up", "Left", "Down", "Right", "Restart", "Exit"]

letter_codes = [ord(c) for c in "WASDQwasdq"]

actions_dict = dict(zip(letter_codes, actions * 2))

def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

#矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]
    

#矩阵逆转（不是矩阵的逆）
def invert(field):
    return [row[::-1] for row in field]
    
class GameField(object):
    def __init__(self, height = 4, width = 4, win = 2048):
        self.height = height    #高 
        self.width = width      #宽
        self.win_score = 2048   #过关分数
        self.score = 0          #当前分数
        self.highest_score = 0  #最高分
        self.reset()            #重置棋盘

    #重置棋盘
    def reset():
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.score = 0
        self.field = [[00 for i in range(self.width)] for i in range(self.height)]
        #一开始棋盘上有两个数字
        self.spawn()
        self.spawn()
    #随机生成2或4
    def spawn(self):
        if randrange(100) > 89:
            new_element = 4
        else:
            new_element = 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element