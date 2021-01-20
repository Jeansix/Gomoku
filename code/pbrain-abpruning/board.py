from collections import Counter
from utils import *

"""
This is a encapsulated version of ab-pruning and utils. It works for test, but I fail to tailor it to the game interface.
My solution is to decompose each method to a independent function. Initialize a board in the strategy and 
"""
# define board
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
depth = 3


class Board:
    def __init__(self, player):
        self.height = MAX_BOARD
        self.width = MAX_BOARD
        self.player = player  # 1 for initial
        self.my_stones = []  # stones for agent
        self.opp_stones = []  # stones for opponent
        self.last_move = None  # conducted by 3-player

    def update_stones(self, board):
        """Update current stones based on the board.
                Args:
                    board: 20*20 array,representing the current state of the game
                Returns:
                    my_stones:list of tuples,my placed stones
                    opp_stones:list of tuples, opponent's placed stones
        """
        my_stones = []
        opp_stones = []
        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] == 1:
                    my_stones.append((i, j))
                elif board[i][j] == 2:
                    opp_stones.append((i, j))
        self.my_stones = my_stones  # lazy fetch strategy
        self.opp_stones = opp_stones

    def get_lines(self, board, pos):
        """Get string lines in four directions based on pos,the expansion center.
            Args:
                board: 20*20 array,representing the current state of the game
                pos: tuple,the center for expansion
            Returns:
                list of strings of patterns
        """
        x, y = pos
        xmin = max(0, x - 4)
        ymin = max(0, y - 4)
        xmax = min(self.height - 1, x + 4)
        ymax = min(self.width - 1, y + 4)
        # extract a sequence from position
        # vertical
        vertical = ''
        for k in range(xmin, xmax+1):
            vertical += str(int(board[k][y]))
        if x - 4 < 0:
            vertical = '*' + vertical
        if x + 4 > self.height - 1:
            vertical = vertical + '*'
        # horizonal
        horizontal = ''
        for k in range(ymin, ymin+1):
            horizontal += str(int(board[x][k]))
        if y - 4 < 0:
            horizontal = '*' + horizontal
        if y + 4 > self.width - 1:
            horizontal = horizontal + '*'
        # diagonal
        diagonal = ''
        for k in range(max(xmin - x, ymin - y), min(xmax - x, ymax - y) + 1):
            diagonal += str(int(board[x + k][y + k]))

        if x - 4 < 0 or y - 4 < 0:
            diagonal = '*' + diagonal

        if x + 4 > self.height - 1 or y + 4 > self.width-1:
            diagonal = diagonal + '*'
        # associate diagonal
        adiagonal = ''
        for k in range(max(xmin - x, y - ymax), min(xmax - x, y - ymin) + 1):
            adiagonal += str(int(board[x + k][y - k]))
        if x - 4 < 0 or y + 4 > self.width - 1:
            adiagonal = '*' + adiagonal
        if x + 4 > self.height - 1 or y - 4 < 0:
            adiagonal = adiagonal + '*'

        return [vertical, horizontal, diagonal, adiagonal]

    # get blank posistions in a radius of distance from pos
    def get_blank_neighbors(self, board, pos, distance):
        """Get neighbours in four directions of pos within distance.
                Args:
                    board: 20*20 array,representing the current state of the game
                    pos: tuple,target position
                    distance:int,size of neighbourhood
                Returns:
                    list of neighbours
        """
        x, y = pos
        neighbors = []
        xmin = x - distance
        xmax = x + distance + 1
        ymin = y - distance
        ymax = y + distance + 1
        for i in range(xmin, xmax):
            if i < 0 or i >= self.height:
                continue
            for j in range(ymin, ymax):
                if j < 0 or j >= self.width:
                    continue
                if i == x and j == y:
                    continue
                if board[i][j] == 0:
                    neighbors.append((i, j))
        return list(set(neighbors))

    # evaluate a move after placing it on the board
    # player==1:use myclassDict
    # player==2:use oppclassDict
    def extract_feature(self, board, player, pos):
        """extract features for current player.
                Args:
                    board: 20*20 array,representing the current state of the game
                    player: 1 for agent's turn, 2 for opponent's turn
                    pos: tuple,target position
                Returns:
                    cnt: a dictionary, representing appearing time for each pattern
        """
        cnt = Counter()
        lines = self.get_lines(board, pos)
        for line in lines:
            if player == 1:
                # how good it is for me
                for key in myclassDict.keys():
                    if key in line:
                        cnt[myclassDict[key]] += 1
                        break
            else:
                # how good it is for me
                for key in oppclassDict.keys():
                    if key in line:
                        cnt[oppclassDict[key]] += 1
                        break
        return cnt

    # evaluate a move for player
    # place it first
    # not calculate value, just roughly sorted
    # after 3-player conducted last_move, player need to pose a stone
    # in other words, we need to sort the interested moves ymin potential
    def filter(self, board, last_move, player, candidates):
        """extract features for current player.
                    Args:
                        board: 20*20 array,representing the current state of the game
                        last_move: tuple, last move conducted by 3-player
                        player: 1 for agent's turn, 2 for opponent's turn
                        candidates: list of tuples, next possible stones
                    Returns:
                        a sorted list for next possible stones
        """
        # if detect win sequence, return immediately
        interested_moves = []
        for pos in candidates:
            x, y = pos
            board[x][y] = player
            score = 0
            # only focus on last two moves
            offend = self.extract_feature(board, player, pos)
            defend = self.extract_feature(board, 3 - player, last_move)
            for pt in offend.keys():
                score += myscoreDict[pt] * offend[pt]
            for pt in defend.keys():
                score -= oppscoreDict[pt] * defend[pt]
            interested_moves.append((pos, score))
            board[x][y] = 0
        interested_moves.sort(key=lambda v: v[1], reverse=True)
        return [x[0] for x in interested_moves]

    def board_evaluation(self, board, player):
        """evaluate current board.
                        Args:
                            board: 20*20 array,representing the current state of the game
                            player: 1 for agent's turn, 2 for opponent's turn
                        Returns:
                            score:int,score for current board,used as value for ab-pruning
        """
        # just after player's turn, who has already placed a stone
        # my_evaluate-opp_evaluate
        score = 0
        self.update_stones(board)
        myCnt = Counter()
        oppCnt = Counter()
        if player == 1:
            # score at each stone
            for pos in self.my_stones:
                mycnt = self.extract_feature(board, player, pos)
                myCnt += mycnt
                for pt in mycnt.keys():
                    score += myscoreDict[pt] * mycnt[pt]
            for pos in self.opp_stones:
                oppcnt = self.extract_feature(board, 3 - player, pos)
                oppCnt += oppcnt
                for pt in oppcnt.keys():
                    score -= oppscoreDict[pt] * oppcnt[pt]
        else:
            # opponent's turn
            # score at each stone
            for pos in self.opp_stones:
                mycnt = self.extract_feature(board, player, pos)
                myCnt += mycnt
                for pt in mycnt.keys():
                    score += myscoreDict[pt] * mycnt[pt]
            for pos in self.my_stones:
                oppcnt = self.extract_feature(board, 3 - player, pos)
                oppCnt += oppcnt
                for pt in oppcnt.keys():
                    score -= oppscoreDict[pt] * oppcnt[pt]
        # print(myCnt,oppCnt)
        return score

    def value_stone(self, board, last_move, alpha, beta, player, level):
        """value a stone.
                    Args:
                        board: 20*20 array,representing the current state of the game
                        last_move: tuple, last move conducted by player
                        alpha: float
                        beta: float
                        player: 1 for agent's turn, 2 for opponent's turn
                        level: current searching depth
                    Returns:
                        value for target stone
        """
        if level >= depth:
            result = self.board_evaluation(board, player)
        else:
            best_move, best_val = self.best_action(board, last_move, alpha, beta, 3 - player, level)
            result = best_val
        return result

    def place_stone(self, board, current_move, alpha, beta, player, level):
        """Place a stone to see its potential.
                    Args:
                        board: 20*20 array,representing the current state of the game
                        current_move: tuple, current move conducted by player
                        alpha: float
                        beta: float
                        player: 1 for agent's turn, 2 for opponent's turn
                        level: current searching depth
                    Returns:
                        a sorted list for next possible stones
        """
        # update the state
        # to see how much score it will attain
        i, j = current_move
        board[i][j] = player
        result = self.value_stone(board, current_move, alpha, beta, player, level)
        board[i][j] = 0 # backtrack
        return result

    def best_action(self, board, last_move, alpha, beta, player, level):
        """Important function for mini-max search with ab-pruning, searching for the best action.
                play=1,representing a max-node
                player=2,representing a min-node

                            Args:
                                board: 20*20 array,representing the current state of the game
                                last_move: tuple, last move conducted by 3-player
                                alpha: float
                                beta: float
                                player: 1 for agent's turn, 2 for opponent's turn
                                level: current searching depth
                            Returns:
                                best_move: tuple
                                best_val:int
        """
        # step1. confirm the candidtates
        candidates = []
        for stone in self.my_stones:
            candidates += self.get_blank_neighbors(board, stone, 1)
        for stone in self.opp_stones:
            candidates += self.get_blank_neighbors(board, stone, 1)
        candidates = list(set(candidates))  # remove duplicates
        self.update_stones(board)
        # step2. filter and roughly sort the candidtates
        # player matters a lot
        # sort in order of my advantage

        interested_moves = self.filter(board, last_move, player, candidates)
        if len(interested_moves) == 1:
            current_move = interested_moves[0]
            val = self.place_stone(board, current_move, alpha, beta, player, level)
            return current_move, val

        # step3. perform ab-pruning
        best_move = interested_moves[0]
        if player == 1:
            # max policy
            max_val = float("-inf")
            for current_move in interested_moves:
                val = self.place_stone(board, current_move, alpha, beta, player, level + 1)
                if val > alpha:
                    alpha = val
                if val > max_val:
                    max_val = val
                    best_move = current_move
                if beta <= alpha:
                    break
            best_val = max_val
        elif player == 2:
            # min policy
            min_val = float("inf")
            for current_move in interested_moves:
                val = self.place_stone(board, current_move, alpha, beta, player, level + 1)
                if val < beta:
                    beta = val
                if val < min_val:
                    min_val = val
                    best_move = current_move
                if beta <= alpha:
                    break
            best_val = min_val
        return best_move, best_val

    def strategy(self, board):
        """Find an optimal action under the current state.
                Args:
                    board:20*20 array,representing the current state of the game
                Returns:
                    best_action: tuple,optimal next action
            """
        if self.last_move is None:
            best_move = (MAX_BOARD // 2, MAX_BOARD // 2)
            x, y = best_move
            board[x][y] = self.player
            self.update_stones(board)
            self.last_move = best_move  # last_move is only updated in the strategy
            return best_move
        # fetch best move from level 0
        level = 0
        alpha = float("-inf")
        beta = float("inf")
        best_move, best_val = self.best_action(board, self.last_move, alpha, beta, 1, level)
        x, y = best_move
        board[x][y] = self.player
        self.last_move = best_move
        # return the best move
        return (best_move[0], best_move[1])


if __name__ == "__main__":
    board_instance = Board(1)
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    stones = [{(11, 11), (10, 12), (12, 10), (13, 9)}, {(10, 10), (10, 13), (9, 13), (11, 13)}]
    playing = 1
    opp_stones = stones[not playing]
    my_stones = stones[playing]
    for pos in opp_stones:
        board[pos[0]][pos[1]] = 2
    for pos in my_stones:
        board[pos[0]][pos[1]] = 1
    for line in board:
        print(line)
    board_instance.update_stones(board)
    board_instance.last_move = (13, 9)
    print(board_instance.strategy(board))
