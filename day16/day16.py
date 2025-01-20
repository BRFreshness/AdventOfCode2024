from gui import *


def main(filename: str):
    stepping = False
    steps_per_click = 1
    loop = True
    draw_text = True

    TIMER_EVENT = pg.USEREVENT + 1

    # number_keys = (pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9)

    c = Course(filename)
    c.find_path(stepping)

    if not stepping:
        print(c.shortest_path())
        print(f"Score: {c[c.end].score}")

    metrics = CourseMetrics(c)
    pg.init()
    display = pg.display.set_mode((metrics.width, metrics.height))

    draw_course(display, c, metrics, draw_text)

    pg.time.set_timer(TIMER_EVENT, 200)

    while loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    loop = False
                    exit()
                if event.key == pg.K_SPACE:
                    if stepping and steps_per_click > 0:
                        c.step_search(steps_per_click)
                        draw_course(display, c, metrics, draw_text)
                if event.key == pg.K_RETURN:
                    stepping = not stepping
                    steps_per_click = 1 if stepping else 0

            if event.type == TIMER_EVENT:
                if not stepping and steps_per_click == 0:
                    c.step_search(1)
                    draw_course(display, c, metrics, draw_text)

        pg.display.flip()

if __name__ == "__main__":
    main("sample1.txt")
    # main("sample2.txt")
    # main("input.txt")
