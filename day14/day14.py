import re
import time

import numpy as np
import pygame as pg

class Robot:
    def __init__(self, x, y, v_x, v_y, map_shape: tuple):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.map_shape = map_shape

    def move(self):
        self.x += self.v_x
        self.x %= self.map_shape[1]
        self.y += self.v_y
        self.y %= self.map_shape[0]

    def __str__(self):
        return f"({self.x},{self.y}) ({self.v_x},{self.v_y})"

def print_area(robots: list[Robot], map_shape: tuple):
    def zeros_to_dots(l: list[int]) -> str:
        l = ["." if c == 0 else str(c) for c in l]
        return "".join(l)
    area = np.full(map_shape, fill_value=0)
    for robot in robots:
        area[robot.y][robot.x] += 1
    for line in area:
        print(zeros_to_dots(line))
    tls, trs, bls, brs = quadrants(area)
    safety_factor = tls * trs * bls * brs
    print(f"{safety_factor=}")
    print("")


def quadrants(area: np.array) -> tuple[int, int, int, int]:
    h = len(area)
    w = len(area[0])
    top_left = np.array([area[i][:w // 2] for i in range(h // 2)])
    top_right = np.array([area[i][w // 2 + 1:] for i in range(h // 2)])
    bot_left = np.array([area[i][:w // 2] for i in range(h // 2 + 1, h)])
    bot_right = np.array([area[i][w // 2 + 1:] for i in range(h // 2 + 1, h)])
    tls = int(top_left.sum())
    trs = int(top_right.sum())
    bls = int(bot_left.sum())
    brs = int(bot_right.sum())
    return tls, trs, bls, brs

def animate(robots: list[Robot], map_shape: tuple):
    pg.init()
    pg.font.init()
    rect = pg.Rect(0, 0, 7, 7)
    factor = 2 if map_shape[0] < 20 else 1
    width = map_shape[1] * rect.width * factor
    height = map_shape[0] * rect.height * factor

    max_tls = 0
    max_trs = 0
    max_bls = 0
    max_brs = 0

    display = pg.display.set_mode((width, height))
    loop = True

    count = 0

    pg.time.set_timer(99, 1)
    display.fill((0, 0, 0))
    while loop:
        # event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    loop = False
                    exit()

            if event.type == 99:
                if count < 7502:
                    count += 1
                    display.fill((0, 0, 0))
                    for robot in robots:
                        robot.move()
                        loc = (robot.x * rect.width * factor, robot.y * rect.height * factor,
                               rect.width, rect.height)
                        pg.Surface.fill(display, (30, 30, 250), loc)
                    area = np.full(map_shape, fill_value=0)
                    for robot in robots:
                        area[robot.y][robot.x] += 1
                    flag = False
                    tls, trs, bls, brs = quadrants(area)
                    if tls > max_tls:
                        max_tls = tls
                        flag = True
                    if trs > max_trs:
                        max_trs = trs
                        flag = True
                    if bls > max_bls:
                        max_bls = bls
                        flag = True
                    if brs > max_brs:
                        max_brs = brs
                        flag = True
                    if flag:
                        print(f":{count=} {max_tls=}, {max_trs=}, {max_bls=}, {max_brs=}")

        pg.display.flip()

def main(map_shape: tuple, filename: str):
    robots = []
    with open(filename) as f:
        for line in f:
            m = [int(val) for val in re.findall(r"([\d-]+)", line)]
            robots.append(Robot(*m, map_shape=map_shape))
            # print(robots[-1])

    print_area(robots, map_shape)
    for _ in range(100):
        for robot in robots:
            robot.move()
    print_area(robots, map_shape)

    # part 2
    # animate while checking the quadrant totals. Find the highest total, then
    # restart and animate until we hit that value. That displays the easter egg and
    # is the answer to the problem.
    animate(robots, map_shape)

if __name__ == '__main__':
    # main((7, 11), "sample.txt")
    main((103,101), "input.txt")