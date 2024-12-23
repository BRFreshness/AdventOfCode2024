import numpy as np

class Trailhead:
    def __init__(self, loc: tuple[int, int], area_map: np.array):
        self.loc = loc
        self.peaks = {}
        self._map = area_map
        self._walk_trail(loc)

    def score(self):
        return len(self.peaks)

    def rating(self):
        return sum([self.peaks[peak] for peak in self.peaks])

    def _add_peak(self, peak: tuple[int, int]):
        if peak not in self.peaks:
            self.peaks[peak] = 0
        self.peaks[peak] += 1

    def _walk_trail(self, loc: tuple[int, int]):
        elevation = int(self._map[*loc])
        if elevation == 9:
            self._add_peak(loc)
            return
        next_elevation = elevation + 1
        north = (loc[0] - 1, loc[1])
        east = (loc[0], loc[1] + 1)
        south = (loc[0] + 1, loc[1])
        west = (loc[0], loc[1] - 1)
        for next_loc in (north, east, south, west):
            if (next_loc[0] < 0 or next_loc[1] < 0 or
                    next_loc[0] >= self._map.shape[0] or
                    next_loc[1] >= self._map.shape[1]):
                continue
            if self._map[*next_loc] == next_elevation:
                self._walk_trail(next_loc)

    def __str__(self):
        return f"{self.loc} score: {self.score()} rating: {self.rating()}"

def main():
    m = []
    with open("input.txt") as f:
        for line in f:
            m.append([int(x) for x in list(line.strip())])
    area_map = np.array(m)
    map_height = area_map.shape[0]
    map_width = area_map.shape[1]
    # find trailheads
    trailheads = []
    for row in range(0, map_height):
       for col in range(0, map_width):
            if area_map[row, col] == 0:
                trailheads.append(Trailhead((row, col), area_map))
    # print(area_map)
    score = 0
    rating = 0
    for trail in trailheads:
        # print(trail)
        score += trail.score()
        rating += trail.rating()
    print(f"Score: {score}, Rating: {rating}")

if __name__ == "__main__":
    main()