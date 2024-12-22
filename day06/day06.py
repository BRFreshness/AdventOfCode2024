import numpy as np
from icecream import ic
from rich.panel import Panel
from rich.console import Console
# from rich.progress import track
console = Console(stderr=True)
console.width = 200
ic.lineWrapWidth = 200

ic.disable()
debug = False

def print_map(input_map: np.ndarray):
    lines = []
    for line in input_map:
        lines.append("".join(list(line)))
    panel = Panel("\n".join(lines), expand=False)
    console.print(panel)
    count_visited(input_map)

def count_visited(course: np.array) -> int:
    visited = 0
    for row in course:
        visited += list(row).count("X")
    ic(visited)
    return visited

def run_course(course: np.array, position: tuple) -> bool:
    visited = {}
    vertical = -1
    horizontal = 0
    while position != (-1, -1):
        course[position[0], position[1]] = "X"

        # check if we've been here before and if we were going in that direction
        if position in visited:
            state = "check"
            ic(state, position, visited[position], (vertical, horizontal))
            for v, h in visited[position]:
                if (v, h) == (vertical, horizontal):
                    state = "loop"
                    ic(state, (v, h) )
                    return True

        # keep track of where we've travelled and which direction
        if position not in visited:
            visited[position] = []
        visited[position].append((vertical, horizontal))
        state = "track"
        ic(state, position, (vertical, horizontal), visited[position])

        next_pos = (position[0] + vertical, position[1] + horizontal)
        if next_pos[0] > course.shape[0]-1 or next_pos[1] > course.shape[1]-1 or next_pos[0] < 0 or next_pos[1] < 0:
            state = "exit"
            ic(state, next_pos, (vertical, horizontal))
            count_visited(course)
            return False
        elif course[next_pos[0], next_pos[1]] == "#" or course[next_pos[0], next_pos[1]] == "O":
            if  course[next_pos[0], next_pos[1]] == "O":
                state = "New obstacle"
                ic(state, next_pos, (vertical, horizontal))
            if horizontal == 0:
                horizontal = -vertical
                vertical = 0
            else:
                vertical = horizontal
                horizontal = 0
            continue
        position = next_pos
    state = "exit 2"
    ic(state, position, (vertical, horizontal))
    count_visited(course)
    return False

def main(search_for_loops: bool = False):
    m = []
    start_position = (-1, -1)
    with open('input.txt') as f:
        row = 0
        for line in f:
            l = list(line.strip())
            m.append(l)
            if '^' in l:
                start_position = (row, l.index('^'))
            row += 1
    course = np.array(m)

    # run the course and count how many locations were visited
    run_course(course, start_position)
    print_map(course)
    print(f"Unique locations visite: {count_visited(course)}")

    if search_for_loops:
        # try placing obstacles at any blank location ('.') and check if the course becomes an infinite loop
        # run_course function returns True in that case. Count how many positions cause infinite loops
        count = 0
        total_checks = course.shape[0] * course.shape[1]
        max_checks = total_checks
        checked = 0
        for col in range(course.shape[1]):
            for row in range(course.shape[0]):
                checked += 1
                if checked > max_checks:
                    break
                course = np.array(m)
                if course[row, col] == ".":
                    course[row, col] = "O"
                    if debug:
                        print_map(course)
                    if run_course(course, start_position):
                        count += 1
                    if debug:
                        print_map(course)
            print(f"{checked*100/total_checks:.2f}% done")
        print(f"Obstacle locations that cause infinite looks: {count}")


if __name__ == "__main__":
    main(True)
