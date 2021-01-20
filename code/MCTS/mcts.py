import pisqpipe as pp
import numpy as np
import random
from copy import deepcopy
from utils import *
from time import time

width = pp.width
height = pp.height
simulate_time = 10
simulate_num = 25


class MCTSNode(object):
    """ node of MCTs.
    Attributes:
        state: tuple, (board, player)
            board: matrix, game board
            player: 1 or 2, next player !!!
                    1: my side
                    2: opposite side
        neighbour: list of step(x, y), step是当前状态下所有空闲8-neighbour
        successor: list of step(x, y), step是当前board下依据某种策略的合法的下一棋步
        suc_node: dictionary {step:node}, node 为经过step后所到达的MCTSNode
        parent: MCSTNode, 上一状态结点
        step: 从parent到self所走的的棋步 (x, y)
        player: 1 or 2, current player
        board: a matrix, current game board
        visit_num : int, time visited
        reward: float (or int)
        prob: 胜率
        isRoot: bool, True iff self is a root
    """

    def __init__(self, state, successor=None, parent=None, step=None):
        self.state = state  # (board, next Player)
        self.neighbour = []
        if not successor:
            self.successor = []
        else:
            self.successor = successor  # list
        self.suc_node = {}  # TODO: 再考虑是否有必要
        self.parent = parent
        self.step = step  # 从parent到该node所走的棋步
        self.player = self.state[1]  # 1 for me, 2 for opponents
        self.board = self.state[0]
        self.visit_num = 0
        self.reward = 0
        self.prob = 0  # 胜率
        self.isRoot = True
        if self.parent:
            self.isRoot = False
        self.updateNeighbour()

    def update(self, newReward):
        """更新结点被访问次数和获胜次数，函数用于back propagation"""
        self.visit_num += 1
        self.reward += newReward

    def isEmpty(self):
        for k in range(height):
            for j in range(width):
                if self.board[k][j]:
                    return False
        return True

    def isBegin(self):
        """判断是否开局, 依据为board是否为空

        Returns:
            bool, True iff it is the board is empty

        """
        if self.parent:  # 有parent则必不空
            return False
        else:
            for k in range(width):
                for j in range(height):
                    if self.board[k][j]:
                        return False
        return True

    def isEnd(self):
        """

        Returns:
            int 0: 未结束
                1: player1 wins
                2: player2 wins
                3: 平局

        """
        if isTerminate(self.board):
            # 假定当前状态为第一次达到五子连珠的状态，因此上一个玩家为胜者
            return 3 - self.player
        elif len(self.successor) == 0:
            return 3
        else:
            return 0

    def updateNeighbour(self):
        """将neighbour更新为已有棋子所有临近位置 8-neighbour."""

        if self.isRoot:
            # 当前为根结点则检查整个board并产生neighbour
            for k in range(height):
                for j in range(width):
                    if self.board[k][j]:
                        self.neighbour.extend(get_free_around((k, j), self.board))
            self.neighbour = list(set(self.neighbour))

        else:
            # 当前为子结点则只需检查最新step
            self.neighbour = deepcopy(self.parent.neighbour)
            self.neighbour.remove(self.step)
            self.successor.extend(get_free_around(self.step, self.board))
            self.successor = list(set(self.successor))

    def sucFromNeighbour(self):
        """以所有neighbour作为successor"""

        self.successor = self.neighbour

    def getSuccessor(self):
        """得到successor"""
        return self.successor

    def isLegalStep(self, step):
        """判断step是否合法(已被占有)

        Args:
            step: (x, y)

        Returns:
            bool

        """
        x, y = step
        if self.board[x][y] == 0:
            return True
        else:
            return False

    def expand(self, step):
        """ 更新suc_node

        Args:
            step: (x, y)

        Returns:
            newNode: an MCTSNode

        """
        parent = deepcopy(self)
        if step not in self.suc_node.keys() and self.isLegalStep(step):
            x, y = step
            # new Node
            newBoard = deepcopy(self.board)
            newBoard[x][y] = self.player
            newState = (newBoard, 3 - self.player)

            newNode = MCTSNode(newState, successor=None, parent=parent, step=step)
            # newNode.updateNeighbour()
            newNode.sucFromNeighbour()
            # 必胜
            if isTerminate(newBoard):
                newNode.prob = 1
            self.suc_node[step] = newNode
        return self.suc_node[step]

    def expandAll(self):
        """扩展所有可能后继结点"""
        for step in self.successor:
            self.expand(step)

    def backPropagate(self, reward):
        """back propagate reward"""
        self.update(reward)
        current = self
        while not current.isRoot:
            reward = 1 - reward
            current = current.parent
            current.update(reward)

    def updateProb(self):
        """ update probability"""
        self.prob = self.reward / self.visit_num
        return self.prob


class simNode(object):
    """比MCTSNode简洁,用于simulate,可以看作是一个过程而非结点"""

    def __init__(self, board, player=1, successor=None):
        """
        Attributes：
        board: current game board
        player: next player, 1 or 2 next!!!
        successor: all 8-neighbours, 因为simulate基本上是随机落子, 所以只需考虑 8-neighbours
        heuristic: [four1, four2, three1, three2], 根据启发函数得到
                   每个元素是一个list, 其中元素为满足对应启发函数的step(x, y)


        """
        self.board = board
        self.player = player  # 下一个走棋的玩家
        if not successor:
            self.successor = []
        else:
            self.successor = successor
        self.heuristic = gen_heuristic(self.board, player)
        # self.four_one = []  # 连续的四个1周围的空位
        # self.four_two = []
        # self.three_one = []
        # self.three_two = []

    def isFull(self):
        """判断棋盘是否已满"""
        return False if self.successor else True

    def isEnd(self):
        """

        Returns:
            an int in {0, 1, 2, 3}
            0: 未结束
            1: player1 wins
            2: player2 wins
            3: 平局

        """
        if isTerminate(self.board):
            return 3 - self.player  # 赢家为上一位玩家
        elif self.isFull():
            return 3  # 平局
        else:
            return 0  # 意味着不是终局

    def nonEmptyHeu(self):
        """

        Returns:
            int in {-1, 0, 1, 2, 3}
                -1: heuristic is empty
                i in {0, 1, 2, 3}: heuristic[i] is te first to be non-empty, 注意考虑了优先级

        """
        if self.player == 1:
            for index in [0, 1, 2, 3]:
                if self.heuristic[index]:
                    return index
            return -1
        elif self.player == 2:
            for index in [1, 0, 3, 2]:
                if self.heuristic[index]:
                    return index
            return -1

    def update_heu(self, step):
        """从step更新heuristic"""
        x, y = step
        # 从heuristic中删除step
        for k in range(4):
            if step in self.heuristic[k]:
                self.heuristic[k].remove(step)
                break  # heuristic 中同一step不会出现两次

        # 按行、列、对角线检查
        # 方便起见，超出范围部分标记为9，使所得列表长度总为11且以(x, y)为中心
        # 以(x, y)为中心，长度为10的一行
        row = [self.board[x][y + j] if (y + j) in range(width) else 9 for j in range(-5, 6)]
        s = ''.join(map(str, row))
        del row
        s = color(s, self.player)
        for j in range(len(s)):
            value = int(s[j])
            if 9 > value > 3:
                self.heuristic[value - 4].append((x, y + j - 5))

        # 以(x, y)为中心，长度为10的一列
        col = [self.board[x + k][y] if (x + k) in range(height) else 9 for k in range(-5, 6)]
        s = ''.join(map(str, col))
        del col
        s = color(s, self.player)
        for k in range(len(s)):
            value = int(s[k])
            if 9 > value > 3:
                self.heuristic[value - 4].append((x + k - 5, y))

        # 以(x, y)为中心，长度为10的对角线
        diag1 = [self.board[x + k][y + k] if (x + k) in range(height) and (y + k) in range(width)
                 else 9 for k in range(-5, 6)]
        s = ''.join(map(str, diag1))
        del diag1
        s = color(s, self.player)
        for k in range(len(s)):
            value = int(s[k])
            if 9 > value > 3:
                self.heuristic[value - 4].append((x + k - 5, y + k - 5))

        # 以(x, y)为中心，长度为10的斜对角线
        diag2 = [self.board[x + j][y - j] if (x + j) in range(height) and (y - j) in range(width)
                 else 9 for j in range(-5, 6)]
        s = ''.join(map(str, diag2))
        del diag2
        s = color(s, self.player)
        for k in range(len(s)):
            value = int(s[k])
            if 9 > value > 3:
                self.heuristic[value - 4].append((x + k - 5, y - k - 5))

    def updateOneStep(self, step):
        """update everything after on step
        Args:
            step: (x, y)

        """
        x, y = step
        # update board
        self.board[x][y] = self.player
        # update successor
        if step in self.successor:
            self.successor.remove(step)
        newSuc = get_free_around(step, self.board)
        self.successor.extend(newSuc)
        self.successor = list(set(self.successor))
        # update heuristic
        self.update_heu(step)
        # player
        self.player = 3 - self.player

    def chooseStep(self):
        """ 选择下一个棋步，优先选择满足启发函数的棋步，否则随机选取successor中元素

        Returns: next step(x, y)

        """
        index = self.nonEmptyHeu()
        if index >= 0:
            newStep = random.choice(self.heuristic[index])
        else:
            newStep = random.choice(self.successor)
        return newStep

    def simulate(self, max_num=simulate_num):
        """从当前状态开始simulate, 假定当前状态不可能是终局

        Args:
            max_num: simulate的最大深度

        Returns:
            0 or 1 : 1 iff win
        """
        beginner = self.player
        for _ in range(max_num):
            # newStep = self.chooseStep()
            # self.updateOneStep(newStep)
            if self.isEnd():  # winner
                if beginner == self.isEnd():
                    return 1
                else:
                    return 0
            newStep = self.chooseStep()
            self.updateOneStep(newStep)
        return 0


def genSimNode(node):
    """generate a simulation node from an MCTSNode

    Args:
        node: a given MCTSNode

    Returns:
        a simNode

    """
    newBoard = deepcopy(node.board)
    newSuc = deepcopy(node.neighbour)
    return simNode(newBoard, node.player, newSuc)


class myMCT(object):
    """大致上是HMCTs"""

    def __init__(self, state):
        self.root = MCTSNode(state)  # 假定不是终局
        # self.current = self.root

    '''
    def strategy(self):
        """获得最优step"""
        candidate = []  # (step, prob)
        self.root.sucFromNeighbour()
        for step in self.root.successor:
            current = self.root.expand(step)
            if current is None:
                continue
            current.sucFromNeighbour()
            if current.prob == 1:
                return step  # 该步必胜
            subCandidate = []
            for subStep in current.successor:
                subCur = current.expand(subStep)
                if subCur.prob == 1:
                    current.prob = 0  # current必输
                    break
                for _ in range(simulate_time):  # simulate_time: 次数
                    sim = genSimNode(subCur)
                    r = sim.simulate(simulate_num)
                    subCur.visit_num += 1
                    subCur.reward += r
                subCur.updateProb()
                subCandidate.append(subCur.prob)
            candidate.append((step, 1 - max(subCandidate)))
        candidate.sort(key=lambda x: x[1], reverse=True)
        return candidate[0][0]
    '''

    def bestStep(self):
        if self.root.isEmpty():
            return height // 2, width // 2
        candidate = []
        self.root.sucFromNeighbour()
        s = genSimNode(self.root)

        if s.nonEmptyHeu() >= 0:
            return random.choice(s.heuristic[s.nonEmptyHeu()])

        t = time()
        for newStep in self.root.successor:
            if time() - t > 30:
                break
            child = self.root.expand(newStep)
            if child.prob == 1:
                return newStep
            # for _ in range(simulate_time):
            #    sim = genSimNode(child)
            #    s = sim.simulate(simulate_num)
            #    reward = 1 - s
            #    child.update(reward)
            time1 = time()
            while time() - time1 <= 1:
                sim = genSimNode(child)
                s = sim.simulate(simulate_num)
                reward = 1 - s
                child.update(reward)
            candidate.append((child.updateProb(), newStep))
        candidate.sort(key=lambda x: x[0], reverse=True)
        if len(candidate) == 0:
            return random.choice(self.root.successor)
        return candidate[0][1]


"""
if __name__ == '__main__':
    a = [[0 for i in range(height)] for j in range(width)]
    a[1][3] = 2
    a[1][4] = 2
    a[1][5] = 2
    a[1][6] = 2
    a[1][7] = 1

    for i in range(4, 8):
        a[i][i] = 2

    # mct = myMCT((a, 1))
    # step = mct.strategy()
    # print(mct.strategy())

    m = MCTSNode((a, 1))
    print(m.neighbour)
    m.sucFromNeighbour()
    print(m.successor)
    sNode = genSimNode(m)

    mct = myMCT((a, 1))
    step = mct.bestStep()
    print(step)
"""
