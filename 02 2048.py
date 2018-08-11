#2048游戏
import curses
#curses不支持Windows系统的解决方案见https://www.jianshu.com/p/953b3a738ee0
from random import randrange, choice
from collections import defaultdict

#设置按键与动作的关系
actions = ["Up", "Left", "Down", "Right", "Restart", "Exit"]
letter_codes = [ord(c) for c in "WASDRQwasdrq"]
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
    def reset(self):
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

    #判断能否移动
    def movable(self, direction):
        #对于其他三个方向的移动，可以将棋盘进行转置或逆转后转化为向左的移动。
        def left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:#可以移动
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:#可以合并
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))
        check = {}
        check["Left"]  = lambda field: any(left_movable(row) for row in field)
        check["Right"] = lambda field: check["Left"](invert(field))
        check["Up"]    = lambda field: check["Left"](transpose(field))
        check["Down"]  = lambda field: check["Right"](transpose(field))
        
        if direction in check:
            return check[direction](self.field)
        else:
            return False

    #判断赢了没
    def win(self):
        return any(any(i >= self.win_score for i in row) for row in self.field)
        
    #判断游戏结束了没
    def gameover(self):
        return not any(self.movable(direction) for direction in actions)
        
    #画棋盘
    def draw(self, screen):
        #游戏的提示信息
        help_string1 = "(W)上 (S)下 (A)左 (D)右"
        help_string2 = "    (R)重置 (Q)退出"
        over_string = "         游戏结束！"
        win_string = "         你赢了！"

        def cast(string):
            screen.addstr(string + "\n")
        
        #画一条水平网格线
        def draw_line():
            #实验楼里这里写了很长，不知道用意是什么
            cast("+------" * self.width + "+")

        def draw_row():
            cast("".join("|{: ^5} ".format(num) if num > 0 else "|      " for num in row) + "|")

        screen.clear()
        cast("分数：" + str(self.score))
        
        if self.highest_score != 0:
            cast("最高分：" + str(self.highest_score))
            
        for row in self.field:
            draw_line()
            draw_row()
        draw_line()
        
        if self.win():
            cast(win_string)
        elif self.gameover():
            cast(over_string)
        else:
            cast(help_string1)
        cast(help_string2)

    def move(self, direction):
        #先定义左移。对于其他三个方向的移动，可以将棋盘进行转置或逆转后转化为向左的移动。
        def move_left(row):
            #把零散的块挤到一起
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
            #合并成对的块
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            #先挤到一起，再合并，最后还要挤到一起
            return tighten(merge(tighten(row)))
        
        moves = {}
        moves["Left"]  = lambda field: [move_left(row) for row in field]
        moves["Right"] = lambda field: invert(moves["Left"](invert(field)))
        moves["Up"]    = lambda field: transpose(moves["Left"](transpose(field)))
        moves["Down"]  = lambda field: transpose(moves["Right"](transpose(field)))
        
        if direction in moves:
            if self.movable(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

def main(stdscr):
    def init():
        #重置棋盘
        game_field.reset()
        return "Game"
        
    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses["Restart"] = "Init"
        responses["Exit"] = "Exit"
        return responses[action]
        
    def game():
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == "Restart":
            return "Init"
        if action == "Exit":
            return "Exit"
        if game_field.move(action):#如果移动成功了的话
            if game_field.win():
                return "Win"
            if game_field.gameover():
                return "GameOver"
        return "Game"
        
    state_actions = {
        "Init": init,
        "Win": lambda: not_game("Win"),
        "GameOver": lambda: not_game("GameOver"),
        "Game": game
    }

    game_field = GameField(win = 2048)
    
    state = "Init"
    #进入状态的循环
    while state != "Exit":
        state = state_actions[state]()
        
curses.wrapper(main)

# 分数：116
# +------+------+------+------+
# |  4   | 16   |  8   |      |
# +------+------+------+------+
# | 16   |  4   |  4   |      |
# +------+------+------+------+
# |  4   |  2   |      |      |
# +------+------+------+------+
# |  2   |      |      |      |
# +------+------+------+------+
# (W)上 (S)下 (A)左 (D)右
#     (R)重置 (Q)退出


#赏花宜对佳人，醉月宜对韵人，映雪宜对高人。