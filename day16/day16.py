from icecream import ic

from gui import *

TIMER_EVENT = pg.USEREVENT + 1

def main(filename: str):
    stepping = True
    steps_per_click = 1
    loop = True
    draw_text = True
    path_list = []

    # number_keys = (pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9)

    course = Course.from_file(filename)
    course.process_floyd_warshall()

    metrics = GridMetrics(course, height=800)
    pg.init()
    display = pg.display.set_mode((metrics.width, metrics.height))

    draw_course(display, course, metrics, draw_text)

    print(f"vertices: {len(course.graph.vertices)}, edges: {len(course.graph.edges)}")
    print(course.graph.vertices)
    course.graph.solve()
    start_loc = course.graph.lookup_vertex(course.start, Headings.EAST)
    start_str = str(course.graph.vertices[start_loc])
    for h, color in [(Headings.EAST, pg.Color("green")), (Headings.NORTH, pg.Color("cyan"))]:
        end_loc = course.graph.lookup_vertex(course.end, h)
        end_str = str(course.graph.vertices[end_loc])
        path, score = course.graph.get_path(start_loc, end_loc)
        print(f"{start_str} to {end_str} : Score={score}, [" + ", ".join([str(course.graph.vertices[loc]) for loc in path]) + "]")
        path_list.append(([course.graph.vertices[loc].loc for loc in path], color))

    course.find_path(stepping)

    if not stepping:
        print(course.shortest_path())
        print(f"Score: {course[course.end].score}")

    pg.time.set_timer(TIMER_EVENT, 100)
    pg.key.set_repeat(500, 30)

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
                        course.step_search(steps_per_click)
                        # draw_course(display, course, metrics, draw_text)
                if event.key == pg.K_RETURN:
                    stepping = not stepping
                    steps_per_click = 1 if stepping else 0
                if event.key == pg.K_KP_PLUS or event.key == pg.K_PLUS or event.key == pg.K_EQUALS:
                    metrics.zoom_in()
                if event.key == pg.K_KP_MINUS or event.key == pg.K_MINUS:
                    metrics.zoom_out()
                if event.key == pg.K_a:
                    metrics.zoom_all()
                if event.key == pg.K_LEFT:
                    metrics.pan_left()
                if event.key == pg.K_RIGHT:
                    metrics.pan_right()
                if event.key == pg.K_UP:
                    metrics.pan_up()
                if event.key == pg.K_DOWN:
                    metrics.pan_down()

            if event.type == TIMER_EVENT:
                if not stepping and steps_per_click == 0:
                    course.step_search(1)
                draw_course(display, course, metrics, draw_text)

                for path, color in path_list:
                    draw_path(display, metrics, path, color)

                for vertex in course.graph.vertices:
                    draw_diamond(display, metrics, vertex.loc, pg.Color("green"))

        pg.display.flip()

if __name__ == "__main__":
    main("sample1.txt")
    # main("sample2.txt")
    # main("sample3.txt")
    # main("input.txt")
