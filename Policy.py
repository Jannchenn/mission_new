# ======================================================================
# FILE:        Policy.py
#
# DESCRIPTION: Contains policies drone will fly including: random, roomba
#
# ======================================================================

from random import randrange, random
from collections import defaultdict
import numpy as np


class Policy:
    def __init__(self, board, start, end, col_dim, row_dim):
        self.q_table = np.random.randint(-2, 20, size=(4, 4, 4, 4))

        self.board = board
        self.start = start
        self.end = end
        self.cur = (0, 0)
        self.dir = 'l'
        self.switch = 0
        self.__colDimension = col_dim
        self.__rowDimension = row_dim
        self.cord_map = change_to_map(board, row_dim * col_dim)

    def random(self):
        """
        This method provides drone to fly randomly
        :reutrn: the tuple of col, row, and wpl
        """
        nei = self._check_neighbor()
        
        next_move = nei[randrange(0, len(nei))]
        c = next_move[0]
        r = next_move[1]
        d = next_move[2]
        self.cur = (c, r)
        self.dir = d
        return c, r, d

    def roomba(self):
        """
        This method provides drone to fly inorder
        :return: the tuple of col, row, and wpl
        """
        temp = (0, 0)
        if self.start[0] == self.end[0]:
            temp = self._horizontal()
        elif self.start[1] == self.end[1]:
            temp = self._vertical()
        if self.switch == 1:
            self.switch = 0
            return self._horizontal()
        elif self.switch == 2:
            self.switch = 0
            return self._vertical()
        return temp

    def get_direction(self):
        return self.dir

    def _horizontal(self):
        """
        returns lat & long
        if at the end: go to vertical (start a new cycle)
        if at the end of some row: turn to the next upper/lower row (depends on dir)
        if at row 0, 2: ------->
        if at row 1, 3: <-------
        """
        c = self.cur[0]
        r = self.cur[1]
        print(c, r)
        d = find_dir(self.start[1], self.end[1])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.__colDimension - 1 - self.start[0], self.end[1])
            self.switch = 2
            return
        if (r % 2 == 0 and c == self.__colDimension - 1) or (r % 2 == 1 and c == 0):
            self.cur = (c, r + d)
            return c, r + d
        if r % 2 == 1:
            self.cur = (c - 1, r)
            return c - 1, r
        if r % 2 == 0:
            self.cur = (c + 1, r)
            return c + 1, r
        else:
            print("nothing\n")

    def _vertical(self):
        """
        returns lat & long
        if at the end: go to horizontal (start a new cycle)
        if at the end of some col: turn to the next left/right col (depends on dir)
        if at col 0, 2: go down
        if at col 1, 3: go up
        """
        c = self.cur[0]
        r = self.cur[1]
        d = find_dir(self.start[0], self.end[0])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.end[0], self.__rowDimension - 1 - self.start[1])
            self.switch = 1
            return
        if (c % 2 == 1 and r == self.__rowDimension - 1) or (c % 2 == 0 and r == 0):
            self.cur = (c + d, r)
            return c + d, r
        if c % 2 == 0:
            self.cur = (c, r - 1)
            return c, r - 1
        if c % 2 == 1:
            self.cur = (c, r + 1)
            return c, r + 1
        else:
            print("nothing")

    def _check_neighbor(self):
        """
        This function checks and return all the neighbors
        :return: list of the valid neighbors(index) that the current position has
        """
        result = []
        c = self.cur[0]
        r = self.cur[1]
        up = (c, r+1, 'u')
        down = (c, r-1, 'd')
        left = (c-1, r, 'l')
        right = (c+1, r, 'r')
        if r+1 < self.__rowDimension:
            result.append(up)
        if r-1 >= 0:
            result.append(down)
        if c-1 >= 0:
            result.append(left)
        if c+1 < self.__rowDimension:
            result.append(right)
        return result


def change_to_coordinate(index):
    """
    Given the index i, returns its corresponding coordinates
    :param index: the index of the list
    :return: the related coordinates
    """
    x = index / 10
    if x % 2 == 0:
        y = index % 10
    else:
        y = 9 - index % 10
        return int(x), int(y)


def change_to_map(board, l):
    """
    Given the board, return a dictionary
    :param board: the board to be transferred
    :param l: total number of sectors
    :return: the dictionary, key: (c,r), val: index
    """
    result = defaultdict(int)
    for i in range(l):
        c = board[i][0]
        r = board[i][1]
        result[(c, r)] = i
    return result


def find_dir(a, b):
    if a < b:
        return 1
    else:
        return -1