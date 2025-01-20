import numpy as np
from enum import StrEnum
from queue import PriorityQueue

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
        self.previous_heading: Headings | None = None
        self.cell_type: CellTypes
        try:
            self.cell_type = CellTypes(cell)
        except ValueError:
            self.cell_type = CellTypes.UNKNOWN

    def __str__(self):
        return self.cell_type.value


class Course:
    def __init__(self, filename: str):
        rows = []
        with open(filename) as f:
            for line in f:
                rows.append(list(line.strip()))
        self.course: np.array(Cell) = np.empty(shape=(len(rows), len(rows[0])), dtype=CellTypes)
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
        self.queue = PriorityQueue()

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
            score, cur_loc, cur_heading = open_list.get()
            cur_cell = self[cur_loc]

            for heading in (Headings.EAST, Headings.WEST, Headings.SOUTH, Headings.NORTH):
                loc = heading.add(cur_loc)
                if loc[0] not in range(self.course.shape[0]) or loc[1] not in range(self.course.shape[1]):
                    continue
                if self[loc].cell_type is CellTypes.WALL:
                    continue

                rot, new_heading = cur_heading.rotations(cur_loc, loc)
                new_score = cur_cell.score + 1 + rot * 1000

                if new_score < self[loc].score:
                    self[loc].score = new_score
                    self[loc].previous_loc = cur_loc
                    self[loc].previous_heading = cur_heading
                    open_list.put((new_score, loc, new_heading))

            if stepping:
                self.cur_loc = cur_loc
                steps -= 1
                if steps < 1:
                    break

        return not open_list.empty()

    def shortest_path(self) -> list:
        """ Returns the path to the end, assuming the board has been filled in via fill_shortest_path """
        loc: tuple | None = self.end
        path = []
        while loc:
            path.append(loc)
            loc = self[loc].previous_loc
        return path

    def __str__(self) -> str:
        return "\n".join(["".join([str(char) for char in line]) for line in self.course])

