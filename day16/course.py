import numpy as np
from enum import StrEnum
from queue import PriorityQueue, Queue
from collections import deque

from floyd_warshall import *
from util import Headings


class CellTypes(StrEnum):
    EMPTY = "."
    WALL = "#"
    START = "S"
    END = "E"
    UNKNOWN = "?"


class Cell:
    def __init__(self, loc: tuple, cell: str):
        self.loc: tuple = loc
        self.score: float = np.inf
        self.previous_loc: tuple | None = None
        self.cell_type: CellTypes
        try:
            self.cell_type = CellTypes(cell)
        except ValueError:
            self.cell_type = CellTypes.UNKNOWN

    def __str__(self):
        return self.cell_type.value


class Course:
    def __init__(self, rows: list, priority: bool = True):
        self.course: np.array(Cell) = np.empty(shape=(len(rows), len(rows[0])), dtype=CellTypes)
        self.priority = priority
        self.start: tuple = (0, 0)
        self.end: tuple = (0, 0)
        for row in range(self.course.shape[0]):
            for col in range(self.course.shape[1]):
                self.course[row][col] = Cell(loc=(row, col), cell=rows[row][col])
                if rows[row][col] == "S":
                    self.start = (row, col)
                if rows[row][col] == "E":
                    self.end = (row, col)
        self.queue: PriorityQueue
        self.cur_loc: tuple | None = None
        self.last_loc: tuple | None = None
        if self.priority:
            self.queue = PriorityQueue()
        else:
            self.queue = Queue()
        self.stepping = False
        self.graph: Graph = Graph()

    @classmethod
    def from_file(cls, filename: str, priority: bool = True):
        rows = []
        with open(filename) as f:
            for line in f:
                rows.append(list(line.strip()))
        instance = cls(rows, priority)
        return instance

    def __getitem__(self, loc: tuple) -> Cell:
        return self.course[loc[0]][loc[1]]

    @property
    def rows(self) -> int:
        return self.course.shape[0]

    @property
    def cols(self) -> int:
        return self.course.shape[1]

    @property
    def shape(self) -> tuple:
        return self.course.shape

    def find_path(self, stepping: bool = False):
        self[self.start].score = 0
        self.queue.put((0, self.start, Headings.EAST))
        if stepping:
            self.step_search(1)
        else:
            self.step_search(0)

    def step_search(self, steps: int = 0) -> bool:
        open_list = self.queue
        stepping = False
        if steps > 0:
            stepping = True

        while not open_list.empty():
            cur_score, cur_loc, cur_heading = open_list.get()

            for new_heading, new_score in ((cur_heading, cur_score + 1),
                                           (cur_heading.cw(), cur_score + 1001),
                                           (cur_heading.ccw(), cur_score + 1001),
                                           (cur_heading.rot180(), cur_score + 2001)):
                new_loc = new_heading.add(cur_loc)
                # print(cur_loc, cur_heading, cur_score, " : " , new_loc, new_heading, new_score)
                # if new_loc[0] not in range(self.course.shape[0]) or new_loc[1] not in range(self.course.shape[1]):
                #     continue
                if self[new_loc].cell_type is CellTypes.WALL:
                    continue

                if new_score < self[new_loc].score:
                    self[new_loc].score = new_score
                    self[new_loc].previous_loc = cur_loc
                    # print("-->", new_score, new_loc, new_heading)
                    open_list.put((new_score, new_loc, new_heading))

            if stepping:
                self.cur_loc = cur_loc
                steps -= 1
                if steps < 1:
                    break

        return not open_list.empty()

    def process_floyd_warshall(self):
        def is_corridor(loc: tuple) -> bool:
            north = loc[0] - 1, loc[1]
            east = loc[0], loc[1] + 1
            south = loc[0] + 1, loc[1]
            west = loc[0], loc[1] - 1
            if (self[north].cell_type is CellTypes.WALL and
                self[south].cell_type is CellTypes.WALL and
                self[west].cell_type is not CellTypes.WALL and
                self[east].cell_type is not CellTypes.WALL) or \
               (self[north].cell_type is not CellTypes.WALL and
                self[south].cell_type is not CellTypes.WALL and
                self[west].cell_type is CellTypes.WALL and
                self[east].cell_type is CellTypes.WALL):
                return True
            return False

        g = self.graph
        for row in range(self.rows):
            for col in range(self.cols):
                cur_loc = (row, col)
                if self[cur_loc].cell_type is CellTypes.WALL or is_corridor(cur_loc):
                    continue

                for cur_h in Headings:
                    u = g.add_vertex(cur_loc, cur_h)
                    for adj_h, score in ((cur_h, 1),
                                         (cur_h.cw(), 1001),
                                         (cur_h.ccw(), 1001)):
                        adj_loc = adj_h.add(cur_loc)
                        while self[adj_loc].cell_type is not CellTypes.WALL:
                            next_loc = adj_h.add(adj_loc)
                            if self[next_loc].cell_type is CellTypes.WALL:
                                break
                            adj_loc = next_loc
                            score += 1
                        if self[adj_loc].cell_type is not CellTypes.WALL:
                            v = g.add_vertex(adj_loc, adj_h)
                            g.add_edge(Edge(u, v, score))
        g.initialize()
        # g.solve()


    def shortest_path(self) -> list:
        """ Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
        loc: tuple | None = self.end
        path = []
        while loc:
            path.append(loc)
            loc = self[loc].previous_loc
        return path

    def traverse_maze(self):
        future_moves = deque()
        good_spots = set()
        dir_map = {
            'u': {'v': (-1, 0), 't': ['l', 'r']}, 'd': {'v': (1, 0), 't': ['l', 'r']},
            'l': {'v': (0, -1), 't': ['u', 'd']}, 'r': {'v': (0, 1), 't': ['u', 'd']}
        }

        def dfs(loc, score, direction, reverse):
            if self[loc].cell_type is CellTypes.WALL or (self[loc].score < score and not reverse):
                return
            if reverse:
                if self[loc].score > score:
                    return
            else:
                if self[loc].cell_type is CellTypes.EMPTY or self[loc].score > score:
                    self[loc].score = score
            if reverse:
                good_spots.add(loc)
            for n_dr in [direction, *dir_map[direction]['t']]:
                n_loc = tuple([loc[i] + dir_map[n_dr]['v'][i] for i in [0, 1]])
                dif = (1001 if n_dr != direction else 1) * (-1 if reverse else 1)
                future_moves.append([n_loc, score + dif, n_dr, reverse])

        future_moves.append([self.start, 0, 'r', False])
        while future_moves:
            dfs(*future_moves.popleft())
        future_moves.append([self.end, self[self.end].score, 'd', True])
        future_moves.append([self.end, self[self.end].score, 'l', True])
        while future_moves:
            dfs(*future_moves.popleft())
        return self[self.end].score, len(good_spots)

    def __str__(self) -> str:
        return "\n".join(["".join([str(char) for char in line]) for line in self.course])

