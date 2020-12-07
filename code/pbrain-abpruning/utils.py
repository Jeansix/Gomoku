# define board
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

# scores for certain patterns
"""
FiveInRow = [1, 1, 1, 1, 1]
LiveFour = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
DeadFour = [[2, 1, 1, 1, 1], [1, 1, 1, 1, 2], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1]]
LiveThree = [[0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1]]
DeadThree = [[2, 1, 1, 1, 0], [0, 1, 1, 1, 2], [2, 1, 1, 0, 1], [1, 0, 1, 1, 2], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1]]
LiveTwo = [[0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0]]
DeadTwo = [[2, 1, 1, 0, 0], [0, 0, 1, 1, 2], [0, 0, 2, 1, 1], [1, 1, 2, 0, 0], [0, 2, 1, 1, 0], [0, 1, 1, 2, 0],
           [2, 1, 0, 1, 0], [0, 1, 0, 1, 2], [0, 2, 1, 0, 1], [1, 0, 1, 2, 0]]
oFiveInRow = [2, 2, 2, 2, 2]
oLiveFour = [[0, 2, 2, 2, 2], [2, 2, 2, 2, 0]]
oDeadFour = [[1, 2, 2, 2, 2], [2, 2, 2, 2, 1], [2, 0, 2, 2, 2], [2, 2, 0, 2, 2], [2, 2, 2, 0, 2]]
oLiveThree = [[0, 2, 2, 2, 0], [0, 2, 0, 2, 2], [2, 0, 2, 2, 0], [2, 2, 0, 2, 0], [0, 2, 2, 0, 2]]
oDeadThree = [[1, 2, 2, 2, 0], [0, 2, 2, 2, 1], [1, 2, 2, 0, 2], [2, 0, 2, 2, 1], [2, 0, 0, 2, 2], [2, 2, 0, 0, 2]]
oLiveTwo = [[0, 0, 2, 2, 0], [0, 2, 2, 0, 0], [0, 2, 0, 2, 0]]
oDeadTwo = [[1, 2, 2, 0, 0], [0, 0, 2, 2, 1], [0, 0, 1, 2, 2], [2, 2, 1, 0, 0], [0, 1, 2, 2, 0], [0, 2, 2, 1, 0],
            [1, 2, 0, 2, 0], [0, 2, 0, 2, 1], [0, 1, 2, 0, 2], [2, 0, 2, 1, 0]]
stoneShapes = [FiveInRow, oFiveInRow, LiveFour, oLiveFour, DeadFour, oDeadFour, LiveThree, oLiveThree, DeadThree,
               oDeadThree, LiveTwo, oLiveTwo, DeadTwo,
               oDeadTwo]
scoreDict = {'FiveInRow': 1e6, 'LiveFour': 1e5, 'DeadFour': 1e4, 'LiveThree': 1e3, 'DeadThree': 1e2, 'LiveTwo': 1e1,
             'DeadTwo': 1, 'oFiveInRow': -1e6, 'oLiveFour': -1e5, 'oDeadFour': -1e4, 'oLiveThree': -1e3,
             'oDeadThree': -1e2, 'oLiveTwo': -1e1,
             'oDeadTwo': -1}
classDict = {0: 'FiveInRow', 2: 'LiveFour', 4: 'DeadFour', 6: 'LiveThree', 8: 'DeadThree', 10: 'LiveTwo',
             12: 'DeadTwo', 1: 'oFiveInRow', 3: 'oLiveFour', 5: 'oDeadFour', 7: 'oLiveThree', 9: 'oDeadThree',
             11: 'oLiveTwo',
             13: 'oDeadTwo'}
             
"""
# mapping sequence score to sum
sumDict = {0: 10, -1: -1e2, -2: -1e3, -3: -3e4, -4: -3e5, -5: -3e6, 1: 1e2, 2: 1e3, 3: 1e4, 4: 1e5, 5: 1e6}


def get_all_around(pos):
    """Get all positions around the given pos.

    Args:
        pos:current position

    Returns:
        list of around positions

    """
    x, y = pos
    return [(nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1]]


def get_board_state(board):
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
