# define board
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

# scores for certain patterns

# mapping sequence score to sum
sumDict = {0: 7, -1: -35, -2: -800, -3: -15000, -4: -800000, -5: -1e7, 1: 15, 2: 400, 3: 1800, 4: 1e5, 5: 1e7}


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


def get_sequence_score(sequence):
    """Score the given sequence
        Args:
            sequence: list,including five stones
        Returns:
            value of score for the sequence.
    """
    if 2 in sequence and 1 in sequence:
        return 0
    # extract sum as feature
    seqTmp = [-1 if x == 2 else x for x in sequence]
    seqSum = sum(seqTmp)
    return sumDict[seqSum]


def get_str_lines(board, point):
    x, y = point
    # vertical
    vertical = ''
    for k in range(max(x - 4, 0), min(x + 5, 20)):
        vertical += str(int(board[k][y]))
    if x - 4 < 0:
        vertical = '*' + vertical
    if x + 4 > 14:
        vertical = vertical + '*'
    # horizonal
    horizontal = ''
    for k in range(max(y - 4, 0), min(y + 5, 20)):
        horizontal += str(int(board[x][k]))
    if y - 4 < 0:
        horizontal = '*' + horizontal
    if y + 4 > 14:
        horizontal = horizontal + '*'
    # diagonal
    diagonal = ''
    bx = max(0, x - 4)
    by = max(0, y - 4)
    ux = min(19, x + 4)
    uy = min(19, y + 4)
    for k in range(max(bx - x, by - y), min(ux - x, uy - y) + 1):
        diagonal += str(int(board[x + k][y + k]))

    if x - 4 < 0 or y - 4 < 0:
        diagonal = '*' + diagonal

    if x + 4 > 19 or y + 4 > 14:
        diagonal = diagonal + '*'
    # associate diagonal
    adiagonal = ''
    for k in range(max(bx - x, y - uy), min(ux - x, y - by) + 1):
        adiagonal += str(int(board[x + k][y - k]))
    if x - 4 < 0 or y + 4 > 19:
        adiagonal = '*' + adiagonal
    if x + 4 > 19 or y - 4 < 0:
        adiagonal = adiagonal + '*'

    return [vertical, horizontal, diagonal, adiagonal]


"""
classDict = {
    "11111": "WIN",
    "011110": "H4",
    "211110": "C4",
    "011112": "C4",
    "*11110": "C4",
    "01111*": "C4",
    "0101110": "C4",
    "0110110": "C4",
    "01110": "H3",
    "010110": "H3",
    "011010": "H3",
    "001112": "M3",
    "00111*": "M3",
    "211100": "M3",
    "*11100": "M3",
    "010112": "M3",
    "01011*": "M3",
    "211010": "M3",
    "*11010": "M3",
    "011012": "M3",
    "01101*": "M3",
    "210110": "M3",
    "*10110": "M3",
    "10011": "M3",
    "11001": "M3",
    "10101": "M3",
    "2011102": "M3",
    "*011102": "M3",
    "201110*": "M3",
    "00110": "H2",
    "01100": "H2",
    "01010": "H2",
    "010010": "H2",
    "000112": "M2",
    "00011*": "M2",
    "211000": "M2",
    "*11000": "M2",
    "001012": "M2",
    "00101*": "M2",
    "210100": "M2",
    "*10100": "M2",
    "010012": "M2",
    "01001*": "M2",
    "210010": "M2",
    "*10010": "M2",
    "10001": "M2",
    "2010102": "M2",
    "201010*": "M2",
    "*010102": "M2",
    "2011002": "M2",
    "*011002": "M2",
    "201100*": "M2",
    "2001102": "M2",
    "200110*": "M2",
    "*001102": "M2",
    "211112": "S4",
    "21111*": "S4",
    "*11112": "S4",
    "21112": "S3",
    "2111*": "S3",
    "*1112": "S3",
    "2112": "S2",
    "*112": "S2",
    "211*": "S2",

    "22222": "oWIN",
    "022220": "oH4",
    "122220": "oC4",
    "022221": "oC4",
    "*22220": "oC4",
    "02222*": "oC4",
    "0202220": "oC4",
    "0220220": "oC4",
    "02220": "oH3",
    "020220": "oH3",
    "022020": "oH3",
    "002221": "oM3",
    "00222*": "oM3",
    "122200": "oM3",
    "*22200": "oM3",
    "020221": "oM3",
    "02022*": "oM3",
    "122020": "oM3",
    "*22020": "oM3",
    "022021": "oM3",
    "02202*": "oM3",
    "120220": "oM3",
    "*20220": "oM3",
    "20022": "oM3",
    "22002": "oM3",
    "20202": "oM3",
    "1022201": "oM3",
    "*022201": "oM3",
    "102220*": "oM3",
    "00220": "oH2",
    "02200": "oH2",
    "02020": "oH2",
    "020020": "oH1",
    "000221": "oM2",
    "00022*": "oM2",
    "122000": "oM2",
    "*22000": "oM2",
    "002021": "oM2",
    "00202*": "oM2",
    "120200": "oM2",
    "*20200": "oM2",
    "020021": "oM2",
    "02002*": "oM2",
    "120020": "M2",
    "*20020": "oM2",
    "20002": "oM2",
    "1020201": "oM2",
    "102020*": "oM2",
    "*020201": "oM2",
    "1022001": "oM2",
    "*022001": "oM2",
    "102200*": "oM2",
    "1002201": "oM2",
    "100220*": "oM2",
    "*002201": "oM2",
    "122221": "oS4",
    "12222*": "oS4",
    "*22221": "oS4",
    "12221": "oS3",
    "1222*": "oS3",
    "*2221": "oS3",
    "1221": "oS2",
    "*221": "oS2",
    "122*": "oS2"
}
scoreDict = {"WIN": 2e5,
             "H4": 1e4,
             "C4": 1e3,
             "H3": 200,
             "M3": 50,
             "H2": 5,
             "M2": 3,
             "S4": -5,
             "S3": -5,
             "S2": -5,
            "oWIN": 2e5,
             "oH4": 1e4,
             "oC4": 1e3,
             "oH3": 200,
             "oM3": 50,
             "oH2": 5,
             "oM2": 3,
             "oS4": -5,
             "oS3": -5,
             "oS2": -5
             }
"""

myclassDict = {
    '11111': 'win5',
    '011110': 'alive4',
    '211110': 'lian-rush4',
    '011112': 'lian-rush4',
    '*11110': 'lian-rush4',
    '01111*': 'lian-rush4',
    '11101': 'tiao-rush4',
    '10111': 'tiao-rush4',
    '11011': 'tiao-rush4',
    '001110': 'lian-alive3',
    '011100': 'lian-alive3',
    '011010': 'tiao-alive3',
    '010110': 'tiao-alive3',
    '211100': 'lian-sleep3',
    '001112': 'lian-sleep3',
    '*11100': 'lian-sleep3',
    '00111*': 'lian-sleep3',
    '211010': 'tiao-sleep3',
    '010112': 'tiao-sleep3',
    '*11010': 'tiao-sleep3',
    '01011*': 'tiao-sleep3',
    '210110': 'tiao-sleep3',
    '011012': 'tiao-sleep3',
    '*10110': 'tiao-sleep3',
    '01101*': 'tiao-sleep3',
    '11001': 'te-sleep3',
    '10011': 'te-sleep3',
    '10101': 'te-sleep3',
    '2011102': 'jia-alive3',
    '*011102': 'jia-alive3',
    '201110*': 'jia-alive3',
    '*01110*': 'jia-alive3',
    '001100': 'alive2',
    '011000': 'alive2',
    '000110': 'alive2',
    '001010': 'alive2',
    '010100': 'alive2',
    '010010': 'alive2',
    '211000': 'sleep2',
    '000112': 'sleep2',
    '*11000': 'sleep2',
    '00011*': 'sleep2',
    '210100': 'sleep2',
    '001012': 'sleep2',
    '*10100': 'sleep2',
    '00101*': 'sleep2',
    '210010': 'sleep2',
    '010012': 'sleep2',
    '*10010': 'sleep2',
    '01001*': 'sleep2',
    '10001': 'sleep2',
    '2010102': 'sleep2',
    '*01010*': 'sleep2',
    '201010*': 'sleep2',
    '*010102': 'sleep2',
    '2011002': 'sleep2',
    '2001102': 'sleep2',
    '*011002': 'sleep2',
    '200110*': 'sleep2',
    '201100*': 'sleep2',
    '*001102': 'sleep2',
    '010': 'alive1'
}
oppclassDict = {
    '22222': 'win5',
    '022220': 'alive4',
    '122220': 'lian-rush4',
    '022221': 'lian-rush4',
    '*22220': 'lian-rush4',
    '02222*': 'lian-rush4',
    '22202': 'tiao-rush4',
    '20222': 'tiao-rush4',
    '22022': 'tiao-rush4',
    '002220': 'lian-alive3',
    '022200': 'lian-alive3',
    '022020': 'tiao-alive3',
    '020220': 'tiao-alive3',
    '122200': 'lian-sleep3',
    '002221': 'lian-sleep3',
    '*22200': 'lian-sleep3',
    '00222*': 'lian-sleep3',
    '122020': 'tiao-sleep3',
    '020221': 'tiao-sleep3',
    '*22020': 'tiao-sleep3',
    '02022*': 'tiao-sleep3',
    '120220': 'tiao-sleep3',
    '022021': 'tiao-sleep3',
    '*20220': 'tiao-sleep3',
    '02202*': 'tiao-sleep3',
    '22002': 'te-sleep3',
    '20022': 'te-sleep3',
    '20202': 'te-sleep3',
    '1022201': 'jia-alive3',
    '*022201': 'jia-alive3',
    '102220*': 'jia-alive3',
    '*02220*': 'jia-alive3',
    '002200': 'alive2',
    '022000': 'alive2',
    '000220': 'alive2',
    '002020': 'alive2',
    '020200': 'alive2',
    '020020': 'alive2',
    '122000': 'sleep2',
    '000221': 'sleep2',
    '*22000': 'sleep2',
    '00022*': 'sleep2',
    '120200': 'sleep2',
    '002021': 'sleep2',
    '*20200': 'sleep2',
    '00202*': 'sleep2',
    '120020': 'sleep2',
    '020021': 'sleep2',
    '*20020': 'sleep2',
    '02002*': 'sleep2',
    '20002': 'sleep2',
    '1020201': 'sleep2',
    '*02020*': 'sleep2',
    '102020*': 'sleep2',
    '*020201': 'sleep2',
    '1022001': 'sleep2',
    '1002201': 'sleep2',
    '*022001': 'sleep2',
    '100220*': 'sleep2',
    '102200*': 'sleep2',
    '*002201': 'sleep2',
    '020': 'alive1'
}

myscoreDict = {"win5": 1e6,
               "alive4": 2e4,
               "lian-rush4": 6100,
               "tiao-rush4": 6000,
               "lian-alive3": 1100,
               "tiao-alive3": 1000,
               "lian-sleep3": 300,
               "tiao-sleep3": 290,
               "te-sleep3": 290,
               "jia-alive3": 290,
               "alive2": 100,
               "sleep2": 10,
               "alive1": 3,
               "nothreat": 1
               }
oppscoreDict = {"win5": 1e6,
                "alive4": 1e5,
                "lian-rush4": 65000,
                "tiao-rush4": 65000,
                "lian-alive3": 5500,
                "tiao-alive3": 5500,
                "lian-sleep3": 200,
                "tiao-sleep3": 200,
                "te-sleep3": 200,
                "jia-alive3": 200,
                "alive2": 90,
                "sleep2": 9,
                "alive1": 4,
                "nothreat": 1
                }
