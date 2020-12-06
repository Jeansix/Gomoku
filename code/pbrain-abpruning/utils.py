# scores for certain patterns
FiveInRow = [1, 1, 1, 1, 1]
LiveFour = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
DeadFour = [[-1, 1, 1, 1, 1], [1, 1, 1, 1, -1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1]]
LiveThree = [[0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [1, 0, 1, 1, 0], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1]]
DeadThree = [[-1, 1, 1, 1, 0], [0, 1, 1, 1, -1], [-1, 1, 1, 0, 1], [1, 0, 1, 1, -1], [1, 0, 0, 1, 1], [1, 1, 0, 0, 1]]
LiveTwo = [[0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0]]
DeadTwo = [[-1, 1, 1, 0, 0], [0, 0, 1, 1, -1], [0, 0, -1, 1, 1], [1, 1, -1, 0, 0], [0, -1, 1, 1, 0], [0, 1, 1, -1, 0],
           [-1, 1, 0, 1, 0], [0, 1, 0, 1, -1], [0, -1, 1, 0, 1], [1, 0, 1, -1, 0]]

scoreDict = {'FiveInRow': 1e6, 'LiveFour': 1e5, 'DeadFour': 1e4, 'LiveThree': 1e3, 'DeadThree': 1e2, 'LiveTwo': 1e1,
             'DeadTwo': 1}
stoneShapes = [FiveInRow, LiveFour, DeadFour, LiveThree, DeadThree, LiveTwo, DeadTwo]

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
