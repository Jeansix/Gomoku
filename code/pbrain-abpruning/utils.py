# define board
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

# scores for certain patterns
FiveInRow = [1, 1, 1, 1, 1]
LiveFour = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
DeadFour = [[2, 1, 1, 1, 1], [1, 1, 1, 1, 2], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1]]
LiveThree = [[0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1]]
DeadThree = [[2, 1, 1, 1, 0], [0, 1, 1, 1, 2], [2, 1, 1, 0, 1], [1, 0, 1, 1, 2], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1]]
LiveTwo = [[0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0]]
DeadTwo = [[2, 1, 1, 0, 0], [0, 0, 1, 1, 2], [0, 0, 2, 1, 1], [1, 1, 2, 0, 0], [0, 2, 1, 1, 0], [0, 1, 1, 2, 0],
           [2, 1, 0, 1, 0], [0, 1, 0, 1, 2], [0, 2, 1, 0, 1], [1, 0, 1, 2, 0]]

stoneShapes = [FiveInRow, LiveFour, DeadFour, LiveThree, DeadThree, LiveTwo, DeadTwo]
scoreDict = {'FiveInRow': 1e6, 'LiveFour': 1e5, 'DeadFour': 1e4, 'LiveThree': 1e3, 'DeadThree': 1e2, 'LiveTwo': 1e1,
             'DeadTwo': 1}
classDict = {0: 'FiveInRow', 1: 'LiveFour', 2: 'DeadFour', 3: 'LiveThree', 4: 'DeadThree', 5: 'LiveTwo',
             6: 'DeadTwo'}


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
