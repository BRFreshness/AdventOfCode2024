import pygame as pg
from course import *


class GridMetrics:
    def __init__(self, course: Course, height: int, width: int | None = None):
        self.course = course
        self.height = height
        self.width = height if width is None else width
        self.spacing = 0
        self.zoom: float = 1.0
        self.view_rows = course.rows
        self.view_cols = course.cols
        self.view_origin = (0, 0)
        self.resize(self.view_rows, self.view_cols)
        self.cell_margin = 1

    @staticmethod
    def calc_dimensions(pixels, num_cells, spacing):
        max_size = 200
        cell_size = (pixels - spacing * (num_cells - 1)) // num_cells
        if cell_size > max_size:
            cell_size = max_size
        outside_margin = pixels - num_cells * cell_size - (num_cells - 1) * spacing
        left_margin = outside_margin // 2
        right_margin = outside_margin - left_margin
        return cell_size, left_margin, right_margin

    # noinspection PyAttributeOutsideInit
    def resize(self, new_rows: int, new_cols: int, new_height: int | None = None, new_width: int | None = None):
        if new_height is not None:
            self.height = new_height
            self.width = new_height if new_width is None else new_width
        self.view_rows = new_rows
        self.view_cols = new_cols
        self.cell_height, self.top_margin, self.bottom_margin = GridMetrics.calc_dimensions(self.height, new_rows, self.spacing)
        self.cell_width, self.left_margin, self.right_margin = GridMetrics.calc_dimensions(self.width, new_cols, self.spacing)
        if self.view_origin[0] + new_rows > self.course.rows:
            self.view_origin = self.course.rows - new_rows, self.view_origin[1]
        if self.view_origin[1] + new_cols > self.course.cols:
            self.view_origin = self.view_origin[0], self.course.cols - new_cols

    def zoom_in(self):
        self.zoom *= 1.5
        rows = int(self.course.rows / self.zoom)
        cols = int(self.course.cols / self.zoom)
        self.resize(rows, cols)

    def zoom_out(self):
        self.zoom /= 1.5
        if self.zoom < 1:
            self.zoom = 1.0
        rows = int(self.course.rows / self.zoom)
        cols = int(self.course.cols / self.zoom)
        self.resize(rows, cols)

    def zoom_all(self):
        self.zoom = 1.0
        self.resize(self.course.rows, self.course.cols)

    def pan_right(self):
        if self.zoom > 1 and self.view_origin[1] < self.course.cols - self.view_cols:
            self.view_origin = self.view_origin[0], self.view_origin[1] + 1

    def pan_left(self):
        if self.zoom > 1 and self.view_origin[1] > 0:
            self.view_origin = self.view_origin[0], self.view_origin[1] - 1

    def pan_up(self):
        if self.zoom > 1 and self.view_origin[0] > 0:
            self.view_origin = self.view_origin[0] - 1, self.view_origin[1]

    def pan_down(self):
        if self.zoom > 1 and self.view_origin[0] < self.course.rows - self.view_rows:
            self.view_origin = self.view_origin[0] + 1, self.view_origin[1]

    def is_visible(self, loc: tuple) -> bool:
        if loc[0] in range(self.view_origin[0], self.view_origin[0] + self.view_rows) and \
                loc[1] in range(self.view_origin[1], self.view_origin[1] + self.view_cols):
            return True
        return False

    def reposition(self, loc: tuple):
        if self.is_visible(loc):
            return
        min_row = self.view_origin[0]
        max_row = self.view_origin[0] + self.view_rows - 1
        min_col = self.view_origin[1]
        max_col = self.view_origin[1] + self.view_cols - 1
        if loc[0] < min_row:
            self.view_origin = loc[0] - 1, self.view_origin[1]
        if loc[0] > max_row:
            self.view_origin = loc[0] - self.view_rows + 2, self.view_origin[1]
        if loc[1] < min_col:
            self.view_origin = self.view_origin[0], loc[1] - 1
        if loc[1] > max_col:
            self.view_origin = self.view_origin[0], loc[1] - self.view_cols + 2

    def cell_rect(self, loc: tuple, margin: bool = False) -> tuple:
        m = self.cell_margin if margin else 0
        return (self.left_margin + loc[1] * self.cell_width + (loc[1] - 1) * self.spacing + m,
                self.top_margin + loc[0] * self.cell_height + (loc[0] - 1) * self.spacing + m,
                self.cell_width - 2*m, self.cell_height - 2*m)

    def cell_center(self, loc: tuple) -> tuple:
        row = loc[0]
        col = loc[1]
        rct = self.cell_rect((row, col))
        return rct[0] + rct[2] // 2, rct[1] + rct[3] // 2

    def view_loc(self, loc: tuple) -> tuple:
        return loc[0] - self.view_origin[0], loc[1] - self.view_origin[1]

    def enumerate(self):
        for row in range(self.view_origin[0], self.view_origin[0] + self.view_rows):
            if row not in range(self.course.rows):
                continue
            for col in range(self.view_origin[1], self.view_origin[1] + self.view_cols):
                if col not in range(self.course.cols):
                    continue
                view_loc = self.view_loc((row, col))
                yield view_loc, (row, col), self.course[(row, col)]


def trans_rect( r, off ):
    return [r[0] + off[0], r[1] + off[1], r[2], r[3]]


def draw_course(surface: pg.Surface, course: Course, metrics: GridMetrics, show_score: bool = False):
    bg_color = pg.Color(0, 0, 0)
    red = pg.Color(220, 40, 40)
    green = pg.Color(40, 220, 40)
    wall_color = pg.Color('firebrick4')
    line_color = pg.Color('yellow')
    line_width = 1
    text_color = pg.Color('white')

    cell_size = min(metrics.cell_height, metrics.cell_width)
    cell_margin = metrics.cell_margin

    if cell_size < 30:
        show_score = False

    # print("\n".join(pg.font.get_fonts()))
    # pg.font.SysFont("calibri", size=20)

    # noinspection SpellCheckingInspection
    cell_font = pg.font.SysFont("robotomononerdfontmono", size=18)

    surface.fill(bg_color)

    for view_loc, loc, cell in metrics.enumerate():
        wall_rect = metrics.cell_rect(view_loc)
        cell_rect = metrics.cell_rect(view_loc, margin=True)

        if cell.cell_type == CellTypes.WALL:
            pg.Surface.fill(surface, wall_color, wall_rect)
        if cell.cell_type == CellTypes.START:
            pg.draw.rect(surface, green, cell_rect, line_width)
        if cell.cell_type == CellTypes.END:
            pg.draw.rect(surface, red, cell_rect, line_width)

        if show_score and cell.score != np.inf:
            cell_score = cell_font.render(f"{cell.score}", True, text_color)
            surface.blit(cell_score, trans_rect(cell_score.get_rect(),
                                            [cell_rect[0] + (cell_rect[2] - cell_score.get_rect()[2]) // 2,
                                             cell_rect[1] + (cell_rect[3] - cell_score.get_rect()[3]) // 2]))
    if course.cur_loc is not None:
        if course.last_loc is not None:
            if course.cur_loc != course.last_loc:
                metrics.reposition(course.cur_loc)
        course.last_loc = course.cur_loc
        pg.draw.circle(surface, line_color, metrics.cell_center(course.cur_loc), cell_size//2, line_width)
        cur_loc =  cell_font.render(f"{course.cur_loc}", True, text_color)
        rect = cur_loc.get_rect()
        surface.blit(cur_loc, trans_rect(rect, [cell_margin, (cell_size - rect.height) // 2]))

    draw_path(surface,metrics, course.shortest_path(), line_color, line_width)


def draw_path(surface: pg.Surface, metrics: GridMetrics, path: list, color: pg.Color, width: int = 1):
    if len(path) < 2:
        return
    for idx in range(len(path)-1):
        loc1 = metrics.view_loc(path[idx])
        loc2 = metrics.view_loc(path[idx+1])
        pg.draw.line(surface, color, metrics.cell_center(loc1), metrics.cell_center(loc2), width)

def draw_diamond(surface: pg.Surface, metrics: GridMetrics, loc: tuple, color: pg.Color, width: int = 1):
    view_loc = metrics.view_loc(loc)
    rect = metrics.cell_rect(view_loc, True)
    center = metrics.cell_center(view_loc)
    diamond = [(center[0], rect[1]), (rect[0], center[1]),
               (center[0], rect[1]+rect[3]), (rect[0]+rect[2], center[1])]
    pg.draw.polygon(surface, color, diamond, width)


def _test():
    for space in range(4):
        for pixels in range(600, 1001, 1):
            for num_cells in range(5, 16, 1):
                cell_size, left_margin, right_margin = GridMetrics.calc_dimensions(pixels, num_cells, space)
                calc_pixels = cell_size * num_cells + space * (num_cells -1) + left_margin + right_margin
                assert calc_pixels == pixels, f"{calc_pixels} != {pixels}"
                assert left_margin >= 0, "Left margin should be non-negative"
                assert right_margin >= 0, "Right margin should be non-negative"

if __name__ == '__main__':
    _test()
