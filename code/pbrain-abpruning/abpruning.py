import utils

depth = 3
MAX_BOARD = 20


def place_stone(board, current_move, alpha, beta, player, level):
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
    result = value_stone(board, current_move, alpha, beta, player, level)
    board[i][j] = 0
    return result


# player has played last move
def value_stone(board, last_move, alpha, beta, player, level):
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
        result = utils.board_evaluation(board, player)  # reach the bottom, conduct board evaluation
    else:
        best_move, best_val = best_action(board, last_move, alpha, beta, 3 - player,
                                          level)
        result = best_val
    return result


def best_action(board, last_move, alpha, beta, player, level):
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
    # step1. confirm the candidtates,8-neighbour
    candidates = []
    my_stones, opp_stones = utils.update_stones(board)
    for stone in my_stones:
        candidates += utils.get_blank_neighbors(board, stone, 1)
    for stone in opp_stones:
        candidates += utils.get_blank_neighbors(board, stone, 1)
    candidates = list(set(candidates))  # remove duplicates

    # step2. filter and roughly sort the candidtates
    # player matters a lot
    # sort in order of my advantage
    interested_moves = utils.filter(board, last_move, player, candidates)
    # interested_moves = candidates
    if len(interested_moves) == 1:
        current_move = interested_moves[0]
        val = place_stone(board, current_move, alpha, beta, player, level)
        return current_move, val

    # step3. perform ab-pruning
    best_move = interested_moves[0]  # continue to play even I'm losing
    if player == 1:
        # max policy
        max_val = float("-inf")
        for current_move in interested_moves:
            val = place_stone(board, current_move, alpha, beta, player, level + 1)
            # killing
            if utils.win(board, last_move, current_move, player):
                best_move = current_move
                best_val = val
                break
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
            val = place_stone(board, current_move, alpha, beta, player, level + 1)
            # killing
            if utils.win(board, last_move, current_move, player):
                best_move = current_move
                best_val = val
                break
            if val < beta:
                beta = val
            if val < min_val:
                min_val = val
                best_move = current_move
            if beta <= alpha:
                break
        best_val = min_val
    return best_move, best_val


def strategy(state):
    """Find an optimal action under the current state.
        Args:
            state: tuple,(stones,playing)
                stones: list of sets,[opp_stones,my_stones]
                       Each is a set contains positions of one player's stones.
                       e.g. my_stones = {(1,1), (1,2), (1,3), (1,4)}
                       serves to reconstruct the board
                playing: 1 or 0
                    indicates whose move it is, with 1 for my turn and 0 for opponent's turn
        Returns:
            best_action: tuple,optimal next action
    """
    # first placed in the center of the board
    if state is None:
        best_move = (MAX_BOARD // 2, MAX_BOARD // 2)
        return best_move
    stones, player = state
    my_stones = stones[player]  # called only when it's the agent's turn
    opp_stones = stones[not player]
    last_move = list(opp_stones)[-1]  # last move is conducted by opponent
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    for i, j in my_stones:
        board[i][j] = 1
    for i, j in opp_stones:
        board[i][j] = 2
    level = 0
    alpha = float("-inf")
    beta = float("inf")
    best_move, best_val = best_action(board, last_move, alpha, beta, 1, level)
    # return the best move
    return (best_move[0], best_move[1])

"""
if __name__ == '__main__':
    # simple test on get_next_stone
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
    state = (stones, playing)
    print(strategy(state))
"""