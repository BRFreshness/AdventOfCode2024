import pygame as pg
from course import *

class CourseMetrics:
    def __init__(self, course: Course,  pixels: int = 1000):
        self.course = course
        self.cell_margin = 1
        self.spacing = 3

        self.cell_size = pixels // self.course.rows
        if self.cell_size > 60:
            self.cell_size = 60
            self.cell_margin = 3
        self.display_size = self.cell_size * self.course.rows

        self.area = (0, 0, self.display_size, self.display_size)
        self.spacing = 0
        self.left = self.area[0] + self.spacing
        self.top = self.area[1] + self.spacing
        self.width = self.area[2] - self.area[0] - 2 * self.spacing
        self.height = self.area[3] - self.area[1] - 2 * self.spacing
        self.cy = self.height / self.course.rows
        self.cx = self.width / self.course.cols

    def cell_rect(self, loc: tuple) -> tuple:
        return self.left + loc[1] * self.cx, self.top + loc[0] * self.cy, self.cx, self.cy

    def cell_center(self, loc: tuple) -> tuple:
        rct = self.cell_rect(loc)
        return rct[0] + rct[2] // 2, rct[1] + rct[3] // 2


def trans_rect( r, off ):
    return [r[0] + off[0], r[1] + off[1], r[2], r[3]]

# def draw_course_section(surface: pg.Surface, course: Course, cell_size: int, cell_margin: int, text: bool = False):
#     pass

def draw_course(surface: pg.Surface, course: Course, metrics: CourseMetrics, show_score: bool = False):
    bg_color = pg.Color(0, 0, 0)
    red = pg.Color(220, 40, 40)
    green = pg.Color(40, 220, 40)
    wall_color = pg.Color('firebrick4')
    line_color = pg.Color('yellow')
    line_width = 1
    text_color = pg.Color('white')

    cell_size = metrics.cell_size
    cell_margin = metrics.cell_margin

    # print("\n".join(pg.font.get_fonts()))
    # pg.font.SysFont("calibri", size=20)

    # noinspection SpellCheckingInspection
    cell_font = pg.font.SysFont("robotomononerdfontmono", size=18)

    surface.fill(bg_color)
    for row, line in enumerate(course.course):
        for col, cell in enumerate(line):
            # wall_loc = (col * cell_size, row * cell_size, cell_size, cell_size)
            wall_loc = metrics.cell_rect((row, col))
            cell_loc = (col * cell_size + cell_margin, row * cell_size + cell_margin,
                        cell_size - 2 * cell_margin, cell_size - 2 * cell_margin)
            if cell.cell_type == CellTypes.WALL:
                pg.Surface.fill(surface, wall_color, wall_loc)
            if cell.cell_type == CellTypes.START:
                pg.draw.rect(surface, green, cell_loc, line_width)
            if cell.cell_type == CellTypes.END:
                pg.draw.rect(surface, red, cell_loc, line_width)

            if show_score and cell.score != np.inf:
                cell_score = cell_font.render(f"{cell.score}", True, text_color)
                surface.blit(cell_score, trans_rect(cell_score.get_rect(),
                                                [cell_loc[0] + (cell_loc[2] - cell_score.get_rect()[2]) // 2,
                                                 cell_loc[1] + (cell_loc[3] - cell_score.get_rect()[3]) // 2]))
    if course.cur_loc is not None:
        pg.draw.circle(surface, line_color, metrics.cell_center(course.cur_loc), cell_size//2, line_width)
        cur_loc =  cell_font.render(f"{course.cur_loc}", True, text_color)
        rect = cur_loc.get_rect()
        surface.blit(cur_loc, trans_rect(rect, [cell_margin, (cell_size - rect.height) // 2]))

    shortest_path = course.shortest_path()
    prev_loc = shortest_path.pop()
    while shortest_path:
        cur_loc = shortest_path.pop()
        pg.draw.line(surface, line_color, metrics.cell_center(prev_loc), metrics.cell_center(cur_loc), line_width)
        prev_loc = cur_loc
