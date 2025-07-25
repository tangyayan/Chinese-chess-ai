import copy
from ChessBoard import *
from Game import *#

class Evaluate(object):
    # 棋子棋力得分
    single_chess_point = {
        'c': 989,   # 车
        'm': 439,   # 马
        'p': 442,   # 炮?
        's': 226,   # 士
        'x': 210,   # 象
        'z': 55,    # 卒
        'j': 65536  # 将
    }
    # 红兵（卒）位置得分
    red_bin_pos_point = [
        [1, 3, 9, 10, 12, 10, 9, 3, 1],
        [18, 36, 56, 95, 118, 95, 56, 36, 18],
        [15, 28, 42, 73, 80, 73, 42, 28, 15],
        [13, 22, 30, 42, 52, 42, 30, 22, 13],
        [8, 17, 18, 21, 26, 21, 18, 17, 8],
        [3, 0, 7, 0, 8, 0, 7, 0, 3],
        [-1, 0, -3, 0, 3, 0, -3, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 红车位置得分
    red_che_pos_point = [
        [185, 195, 190, 210, 220, 210, 190, 195, 185],
        [185, 203, 198, 230, 245, 230, 198, 203, 185],
        [180, 198, 190, 215, 225, 215, 190, 198, 180],
        [180, 200, 195, 220, 230, 220, 195, 200, 180],
        [180, 190, 180, 205, 225, 205, 180, 190, 180],
        [155, 185, 172, 215, 215, 215, 172, 185, 155],
        [110, 148, 135, 185, 190, 185, 135, 148, 110],
        [100, 115, 105, 140, 135, 140, 105, 115, 110],
        [115, 95, 100, 155, 115, 155, 100, 95, 115],
        [20, 120, 105, 140, 115, 150, 105, 120, 20]
    ]
    # 红马位置得分
    red_ma_pos_point = [
        [80, 105, 135, 120, 80, 120, 135, 105, 80],
        [80, 115, 200, 135, 105, 135, 200, 115, 80],
        [120, 125, 135, 150, 145, 150, 135, 125, 120],
        [105, 175, 145, 175, 150, 175, 145, 175, 105],
        [90, 135, 125, 145, 135, 145, 125, 135, 90],
        [80, 120, 135, 125, 120, 125, 135, 120, 80],
        [45, 90, 105, 190, 110, 90, 105, 90, 45],
        [80, 45, 105, 105, 80, 105, 105, 45, 80],
        [20, 45, 80, 80, -10, 80, 80, 45, 20],
        [20, -20, 20, 20, 20, 20, 20, -20, 20]
    ]
    # 红炮位置得分
    red_pao_pos_point = [
        [190, 180, 190, 70, 10, 70, 190, 180, 190],
        [70, 120, 100, 90, 150, 90, 100, 120, 70],
        [70, 90, 80, 90, 200, 90, 80, 90, 70],
        [60, 80, 60, 50, 210, 50, 60, 80, 60],
        [90, 50, 90, 70, 220, 70, 90, 50, 90],
        [120, 70, 100, 60, 230, 60, 100, 70, 120],
        [10, 30, 10, 30, 120, 30, 10, 30, 10],
        [30, -20, 30, 20, 200, 20, 30, -20, 30],
        [30, 10, 30, 30, -10, 30, 30, 10, 30],
        [20, 20, 20, 20, -10, 20, 20, 20, 20]
    ]
    # 红将位置得分
    red_jiang_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9750, 9800, 9750, 0, 0, 0],
        [0, 0, 0, 9900, 9900, 9900, 0, 0, 0],
        [0, 0, 0, 10000, 10000, 10000, 0, 0, 0],
    ]
    # 红相或士位置得分
    red_xiang_shi_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 60, 0, 0, 0, 60, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 80, 90, 80, 0, 0, 80],
        [0, 0, 0, 0, 0, 120, 0, 0, 0],
        [0, 0, 70, 100, 0, 100, 70, 0, 0],
    ]

    red_pos_point = {
        'z': red_bin_pos_point,
        'm': red_ma_pos_point,
        'c': red_che_pos_point,
        'j': red_jiang_pos_point,
        'p': red_pao_pos_point,
        'x': red_xiang_shi_pos_point,
        's': red_xiang_shi_pos_point
    }

    def __init__(self, team):
        self.team = team

    def get_single_chess_point(self, chess: Chess):
        if chess.team == self.team:
            return self.single_chess_point[chess.name]
        else:
            return -1 * self.single_chess_point[chess.name]

    def get_chess_pos_point(self, chess: Chess):
        red_pos_point_table = self.red_pos_point[chess.name]
        if chess.team == 'r':
            pos_point = red_pos_point_table[chess.row][chess.col]
        else:
            pos_point = red_pos_point_table[9 - chess.row][chess.col]
        if chess.team != self.team:
            pos_point *= -1
        return pos_point

    def evaluate(self, chessboard: ChessBoard):
        point = 0
        for chess in chessboard.get_chess():
            point += self.get_single_chess_point(chess)
            point += self.get_chess_pos_point(chess)
        return point


class ChessMap(object):
    def __init__(self, chessboard: ChessBoard):
        self.chess_map = copy.deepcopy(chessboard.chessboard_map)


class ChessAI(object):
    def __init__(self, computer_team):
        self.team = computer_team
        self.evaluate_class = Evaluate(self.team)
    
    def now_player(self,gameplayer):
        if self.team=='r':op='b'
        else:op='r'
        if gameplayer==1:return op
        else:return self.team

    def self_movechess(self,chessboard,old_row,old_col,new_row,new_col):
        # 移动位置
        chessboard.chessboard_map[new_row][new_col] = chessboard.chessboard_map[old_row][old_col]
        # 修改棋子的属性
        chessboard.chessboard_map[new_row][new_col].update_position(new_row, new_col)
        # 清楚之前位置为None
        chessboard.chessboard_map[old_row][old_col] = None

    def alpha_beta(self,chessboard,gameplayer,alpha,beta,back_button,depth):#return present_goat,0表示alpha(max,myself),1表示beta
        if chessboard.judge_draw() or back_button.is_repeated():
            return self.evaluate_class.evaluate(chessboard)
        if chessboard.judge_attack_general(self.now_player(1-gameplayer)) and chessboard.judge_win(self.now_player(1-gameplayer)): 
            #print("y")
            return self.evaluate_class.evaluate(chessboard)
        if chessboard.judge_win(self.now_player(1-gameplayer)):
            #print("y")
            return self.evaluate_class.evaluate(chessboard)
        if depth==0:return self.evaluate_class.evaluate(chessboard) 

        for chess in chessboard.get_chess():#除去不是本方
            if chess.team!=self.now_player(gameplayer):continue
            for put_down_chess in chessboard.get_put_down_position(chess):
                #(chess, put_down_chess)
                #print(depth)
                #if depth==0:print(depth,chess.team+"_"+chess.name)
                """
                new_chessboard=chessboard.set_state()
                ClickBox(new_chessboard.screen,chess.row,chess.col)
                new_chessboard.move_chess(put_down_chess[0],put_down_chess[1],is_print=False)
                ClickBox.clean()
                """
                #print("1")
                #for str in chessboard.get_chessboard_str_map():
                #    print(str)
                original_row, original_col = chess.row, chess.col
                target_chess=chessboard.chessboard_map[put_down_chess[0]][put_down_chess[1]]
                self.self_movechess(chessboard,chess.row,chess.col,put_down_chess[0],put_down_chess[1])
                back_button.add_history(chessboard.get_chessboard_str_map())

                now_goat=self.alpha_beta(chessboard,1-gameplayer,alpha,beta,back_button,depth-1)

                #---回溯时还原状态,不能这样回溯，应该用悔棋的哪个函数，这样回溯会导致吃棋回不来
                back_button.pop_history()
                self.self_movechess(chessboard,put_down_chess[0],put_down_chess[1],original_row,original_col)
                if target_chess!=None:
                    chessboard.chessboard_map[put_down_chess[0]][put_down_chess[1]]=target_chess
                #print("2")
                #for str in chessboard.get_chessboard_str_map():
                #    print(str)

                if gameplayer==0:
                    alpha=max(alpha,now_goat)
                    if alpha>=beta:break
                    #alpha=max(alpha,ab_value)
                else:
                    beta=min(beta,now_goat)
                    if beta<=alpha:break
                    #beta=min(beta,ab_value)
            
            #if alpha>=beta:return ab_value
            if alpha>=beta:break

        if gameplayer==0:return alpha
        else: return beta          

    def get_next_step(self, chessboard: ChessBoard):
        best_choice=None
        best_goat=None
        back_button=BackChess(chessboard.screen)
        back_button.add_history(chessboard.get_chessboard_str_map())
        len_wait=0
        for chess in chessboard.get_chess():
            if chess.team!=self.team:continue
            len_wait+=len(chessboard.get_put_down_position(chess))

        for chess in chessboard.get_chess():
            if chess.team!=self.team:continue
            #print(chess.team+"_"+chess.name)
            for put_down_chess in chessboard.get_put_down_position(chess):
                """
                new_chessboard=chessboard.set_state()
                ClickBox(new_chessboard.screen,chess.row,chess.col)
                new_chessboard.move_chess(put_down_chess[0],put_down_chess[1],is_print=False)
                ClickBox.clean()
                back_button.add_history(new_chessboard.get_chessboard_str_map())
                """
                original_row, original_col = chess.row, chess.col
                target_chess=chessboard.chessboard_map[put_down_chess[0]][put_down_chess[1]]
                self.self_movechess(chessboard,chess.row,chess.col,put_down_chess[0],put_down_chess[1])
                back_button.add_history(chessboard.get_chessboard_str_map())

                max_dep=3
                if len_wait<=30:max_dep=4
                now_goat=self.alpha_beta(chessboard,1,-float("inf"),float("inf"),back_button,2)
                if not best_goat or best_goat<now_goat:
                    best_goat=now_goat
                    best_choice=(chess,put_down_chess)

                self.self_movechess(chessboard,put_down_chess[0],put_down_chess[1],original_row,original_col)
                if target_chess!=None:
                    chessboard.chessboard_map[put_down_chess[0]][put_down_chess[1]]=target_chess

                back_button.pop_history()
        tar_chess,tar_put_down_chess=best_choice
        return tar_chess.row,tar_chess.col,tar_put_down_chess[0],tar_put_down_chess[1]
