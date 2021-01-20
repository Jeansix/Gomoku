# IMPORTS
from collections import Counter

# HYPER PARAMETER
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
depth = 3

# scores for certain patterns
# mapping sequence score to sum
# sumDict = {0: 7, -1: -35, -2: -800, -3: -15000, -4: -800000, -5: -1e7, 1: 15, 2: 400, 3: 1800, 4: 1e5, 5: 1e7}
myclassDict = {
    '11111': 'H5',
    '011110': 'H4',
    '211110': 'B4',
    '011112': 'B4',
    '*11110': 'B4',
    '01111*': 'B4',
    '11101': 'B4',
    '10111': 'B4',
    '11011': 'B4',
    '001110': 'H3',
    '011100': 'H3',
    '011010': 'H3',
    '010110': 'H3',
    '211100': 'B3',
    '001112': 'B3',
    '*11100': 'B3',
    '00111*': 'B3',
    '211010': 'B3',
    '010112': 'B3',
    '*11010': 'B3',
    '01011*': 'B3',
    '210110': 'B3',
    '011012': 'B3',
    '*10110': 'B3',
    '01101*': 'B3',
    '11001': 'B3',
    '10011': 'B3',
    '10101': 'B3',
    '001100': 'H2',
    '011000': 'H2',
    '000110': 'H2',
    '001010': 'H2',
    '010100': 'H2',
    '010010': 'H2',
    '211000': 'B2',
    '000112': 'B2',
    '*11000': 'B2',
    '00011*': 'B2',
    '210100': 'B2',
    '001012': 'B2',
    '*10100': 'B2',
    '00101*': 'B2',
    '210010': 'B2',
    '010012': 'B2',
    '*10010': 'B2',
    '01001*': 'B2',
    '10001': 'B2',
    '2010102': 'B2',
    '*01010*': 'B2',
    '201010*': 'B2',
    '*010102': 'B2',
    '2011002': 'B2',
    '2001102': 'B2',
    '*011002': 'B2',
    '200110*': 'B2',
    '201100*': 'B2',
    '*001102': 'B2',
    '010': 'H1'
}
oppclassDict = {
    '22222': 'H5',
    '022220': 'H4',
    '122220': 'B4',
    '022221': 'B4',
    '*22220': 'B4',
    '02222*': 'B4',
    '22202': 'B4',
    '20222': 'B4',
    '22022': 'B4',
    '002220': 'H3',
    '022200': 'H3',
    '022020': 'H3',
    '020220': 'H3',
    '122200': 'B3',
    '002221': 'B3',
    '*22200': 'B3',
    '00222*': 'B3',
    '122020': 'B3',
    '020221': 'B3',
    '*22020': 'B3',
    '02022*': 'B3',
    '120220': 'B3',
    '022021': 'B3',
    '*20220': 'B3',
    '02202*': 'B3',
    '22002': 'B3',
    '20022': 'B3',
    '20202': 'B3',
    '002200': 'H2',
    '022000': 'H2',
    '000220': 'H2',
    '002020': 'H2',
    '020200': 'H2',
    '020020': 'H2',
    '122000': 'B2',
    '000221': 'B2',
    '*22000': 'B2',
    '00022*': 'B2',
    '120200': 'B2',
    '002021': 'B2',
    '*20200': 'B2',
    '00202*': 'B2',
    '120020': 'B2',
    '020021': 'B2',
    '*20020': 'B2',
    '02002*': 'B2',
    '20002': 'B2',
    '1020201': 'B2',
    '*02020*': 'B2',
    '102020*': 'B2',
    '*020201': 'B2',
    '1022001': 'B2',
    '1002201': 'B2',
    '*022001': 'B2',
    '100220*': 'B2',
    '102200*': 'B2',
    '*002201': 'B2',
    '020': 'H1'
}

# score dict for the current player(agent,opponent)
myscoreDict = {"H5": 1e6,
               "H4": 2e4,
               "B4": 6e3,
               "H3": 1e3,
               "B3": 300,
               "H2": 100,
               "B2": 10,
               "H1": 1,
               }

# score dict for the next player(agent,opponent)
oppscoreDict = {"H5": 1e6,
                "H4": 1e5,
                "B4": 6e4,
                "H3": 5e3,
                "B3": 200,
                "H2": 100,
                "B2": 10,
                "H1": 1,
                }

"""
# sum version of board_evaluation
def board_evaluation(state):
    Evaluate the current board at the leaf node.
        Args:
            state: tuple,(stones,playing)
        Returns:
    stones, playing = state
    # Step1. Restore the board
    # 1 for occupied by self, 2 for occupied by opponent, 0 for empty position
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            # if occupied by opponent
            if (i, j) in stones[not playing]:
                board[i][j] = 2
            # if occupied by self
            elif (i, j) in stones[playing]:
                board[i][j] = 1
    # Step2. Evaluate the board
    # Detect whether the sequence falls into the following seven categories
    # FiveInRow,LiveFour,DeadFour,LiveThree,DeadThree,LiveTwo,DeadTwo
    boardEval = 0
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            # find suitable sequence in four directions
            # vertical line
            if j + 4 < MAX_BOARD:
                sequence = [board[i][k] for k in range(j, j + 5)]  # extract sequence by slice
                boardEval += get_sequence_score(sequence)
            # horizontal line
            if i + 4 < MAX_BOARD:
                sequence = [board[k][j] for k in range(i, i + 5)]
                boardEval += get_sequence_score(sequence)
            # main diagonal line
            if i + 4 < MAX_BOARD and j + 4 < MAX_BOARD:
                sequence = []
                for k in range(5):
                    sequence.append(board[i + k][j + k])
                boardEval += get_sequence_score(sequence)
            # associate diagonal line
            if i + 4 < MAX_BOARD and j - 4 >= 0:
                sequence = []
                for k in range(5):
                    sequence.append(board[i + k][j - k])
                boardEval += get_sequence_score(sequence)
    return boardEval
"""

"""
def get_sequence_score(sequence):

Score the given sequence
Args:
sequence: list, including five stones
Returns:value of score for the sequence. 
    if 2 in sequence and 1 in sequence:
        return 0
# extract sum as feature
    seqTmp = [-1 if x == 2 else x for x in sequence]
    seqSum = sum(seqTmp)
    return sumDict[seqSum]
"""


def get_board_state(board):
    """Get board state(stones,playing) from board,an interface with pisqpipe.
            Args:
                board: 20*20 array,representing the current state of the game
            Returns:
                state: tuple,(stones,playing)
                    stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
                    playing: 1 or 0
                        indicates whose move it is, with 1 for my turn and 0 for opponent's turn
    """
    isStart = True
    my_stones = set()
    opp_stones = set()
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            # my stone
            if board[i][j] == 1:
                my_stones.add((i, j))
                isStart = False
            elif board[i][j] == 2:
                opp_stones.add((i, j))
                isStart = False
    if isStart is True:
        return None
    else:
        playing = 1  # called only when it's my turn
        stones = [opp_stones, my_stones]
        state = (stones, playing)
        return state


def update_stones(board):
    """Update current stones based on the board.
            Args:
                board: 20*20 array,representing the current state of the game
            Returns:
                my_stones:list of tuples,my placed stones
                opp_stones:list of tuples, opponent's placed stones
    """
    my_stones = []
    opp_stones = []
    for i in range(20):
        for j in range(20):
            if board[i][j] == 1:
                my_stones.append((i, j))
            elif board[i][j] == 2:
                opp_stones.append((i, j))
    return my_stones, opp_stones


def get_lines(board, pos):
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
    xmax = min(MAX_BOARD - 1, x + 4)
    ymax = min(MAX_BOARD - 1, y + 4)
    # vertical ——
    vertical = ''
    for k in range(xmin, xmax+1):
        vertical += str(int(board[k][y]))
    if x - 4 < 0:
        vertical = '*' + vertical
    if x + 4 > MAX_BOARD:
        vertical = vertical + '*'
    # horizonal |
    horizontal = ''
    for k in range(ymin, ymin+1):
        horizontal += str(int(board[x][k]))
    if y - 4 < 0:
        horizontal = '*' + horizontal
    if y + 4 > MAX_BOARD:
        horizontal = horizontal + '*'
    # diagonal /
    diagonal = ''
    for k in range(max(xmin - x, ymin - y), min(xmax - x, ymax - y) + 1):
        diagonal += str(int(board[x + k][y + k]))

    if x - 4 < 0 or y - 4 < 0:
        diagonal = '*' + diagonal

    if x + 4 > MAX_BOARD - 1 or y + 4 > MAX_BOARD - 1:
        diagonal = diagonal + '*'
    # associate diagonal \
    adiagonal = ''
    for k in range(max(xmin - x, y - ymax), min(xmax - x, y - ymin) + 1):
        adiagonal += str(int(board[x + k][y - k]))
    if x - 4 < 0 or y + 4 > MAX_BOARD - 1:
        adiagonal = '*' + adiagonal
    if x + 4 > MAX_BOARD - 1 or y - 4 < 0:
        adiagonal = adiagonal + '*'

    return [vertical, horizontal, diagonal, adiagonal]


def get_blank_neighbors(board, pos, distance):
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
        if i < 0 or i >= MAX_BOARD:
            continue
        for j in range(ymin, ymax):
            if j < 0 or j >= MAX_BOARD:
                continue
            if i == x and j == y:
                continue
            if board[i][j] == 0:
                neighbors.append((i, j))
    return list(set(neighbors))


# player indicates whose class dictionary to refer to
def extract_feature(board, player, pos):
    """extract features for current player.
            Args:
                board: 20*20 array,representing the current state of the game
                player: 1 for agent's turn, 2 for opponent's turn
                pos: tuple,target position
            Returns:
                cnt: a dictionary, representing appearing time for each pattern
    """
    cnt = Counter()
    lines = get_lines(board, pos)
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


# player has just conducted current_move
# 3-player has just conducted last_move
def win(board, last_move, current_move, player):
    """quick judge of will win sequence .
                    Args:
                        board: 20*20 array,representing the current state of the game
                        last_move: tuple, last move conducted by 3-player
                        current_move: tuple, last move conducted by player
                        player: 1 for agent's turn, 2 for opponent's turn
                    Returns:
                        bool
        """
    mycnt = extract_feature(board, player, current_move)
    oppcnt = extract_feature(board, 3 - player, last_move)  # locality
    if mycnt['H5'] > 0:
        return True
    if mycnt['H4'] and oppcnt['H4'] + oppcnt['B4'] == 0:
        return True
    return False


def filter(board, last_move, player, candidates):
    """extract features for current player.
                Args:
                    board: 20*20 array,representing the current state of the game
                    last_move: tuple, last move conducted by 3-player
                    player: 1 for agent's turn, 2 for opponent's turn
                    candidates: list of tuples, next possible stones
                Returns:
                    a sorted list for next possible stones
    """
    interested_moves = []
    for pos in candidates:
        x, y = pos
        board[x][y] = player
        score = 0
        # only focus on last two moves
        offend = extract_feature(board, player, pos)
        defend = extract_feature(board, 3 - player, last_move)
        for pt in offend.keys():
            score += myscoreDict[pt] * offend[pt]
        for pt in defend.keys():
            score -= oppscoreDict[pt] * defend[pt]
        interested_moves.append((pos, score))
        board[x][y] = 0
    interested_moves.sort(key=lambda v: v[1], reverse=True)
    return [x[0] for x in interested_moves]


def board_evaluation(board, player):
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
    my_stones, opp_stones = update_stones(board)
    myCnt = Counter()
    oppCnt = Counter()
    if player == 1:
        # score at each stone
        for pos in my_stones:
            mycnt = extract_feature(board, player, pos)
            myCnt += mycnt
            for pt in mycnt.keys():
                score += myscoreDict[pt] * mycnt[pt]
        for pos in opp_stones:
            oppcnt = extract_feature(board, 3 - player, pos)
            oppCnt += oppcnt
            for pt in oppcnt.keys():
                score -= oppscoreDict[pt] * oppcnt[pt]
    else:
        # opponent's turn
        # score at each stone
        for pos in opp_stones:
            mycnt = extract_feature(board, player, pos)
            myCnt += mycnt
            for pt in mycnt.keys():
                score += myscoreDict[pt] * mycnt[pt]
        for pos in my_stones:
            oppcnt = extract_feature(board, 3 - player, pos)
            oppCnt += oppcnt
            for pt in oppcnt.keys():
                score -= oppscoreDict[pt] * oppcnt[pt]
    # print(myCnt,oppCnt)

    return score
