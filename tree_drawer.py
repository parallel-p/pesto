import drawer
import math
import sys


BACKGROUND_COLOR = "white"

PROBLEM_SIZE_X = 200
PROBLEM_SIZE_Y = 50
PROBLEM_FILL_COLOR = "yellow"
PROBLEM_BORDER_COLOR = "black"
PROBLEM_BORDER_THICKNESS = 2

PROBLEM_Y_INTERVAL = 200
PROBLEM_X_MIN_INTERVAL = 100
TOP_BOTTOM_SPACE = 50

TREE_LINE_THICKNESS = 4
TREE_LINE_COLOR = "red"

LOCATE_LINES_MAX_SPEED = 8.0
LOCATE_LINES_MAX_SPEED_SQR = LOCATE_LINES_MAX_SPEED ** 2
LOCATE_LINES_PROBLEMS_FORCE = -10000.0
LOCATE_LINES_DESTINATION_CONSTANT_FORCE = 4.0

LOCATE_LINES_LINE_CONSTANT_FORCE = 2.5
LOCATE_LINES_LINE_FORCE_DISTANCE = 20


def _is_point_in_rectangle(point, rect_start, rect_size):
    return rect_start[0] <= point[0] <= rect_start[0] + rect_size[0] and \
        rect_start[1] <= point[1] <= rect_start[1] + rect_size[1]


def _distance_sqr(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x * x + y * y


def _vector_length_sqr(v):
    return v[0] * v[0] + v[1] * v[1]


def _normalize(v):
    length = _vector_length_sqr(v) ** 0.5
    return (v[0] / length, v[1] / length)


def _point_rectangle_distance_sqr(point, rect_begin, rect_size):
    rect_end = (rect_begin[0] + rect_size[0], rect_begin[1] + rect_size[1])
    if point[0] < rect_begin[0]:
        if point[1] < rect_begin[1]:
            return _distance_sqr(point, rect_begin)
        elif point[1] > rect_end[1]:
            return _distance_sqr(point, (rect_begin[0], rect_end[1]))
        else:
            return (rect_begin[0] - point[0]) ** 2
    elif point[0] > rect_end[0]:
        if point[1] < rect_begin[1]:
            return _distance_sqr(point, (rect_end[0], rect_begin[1]))
        elif point[1] > rect_end[1]:
            return _distance_sqr(point, rect_end)
        else:
            return (point[0] - rect_end[0]) ** 2
    elif point[1] < rect_begin[1]:
        return (rect_begin[1] - point[1]) ** 2
    else:
        return (point[1] - rect_end[1]) ** 2
    # center = (point[0] + rect_size[0] / 2, point[1] + rect_size[1] / 2)
    # vec_w = (point[0] - center[0], (point[1] - center[1]) * PROBLEM_SIZE_Y / PROBLEM_SIZE_X)
    # return _distance_sqr(vec_w) ** 0.5 - PROBLEM_SIZE_X / 2 *


class TreeDrawer:
    def __init__(self, tree):
        self.tree = tree
        self.problems = self.tree.get_problems()
        self.contests = []
        current_contest_id = ''
        for problem in self.problems:
            if problem.problem_id[0] != current_contest_id:
                current_contest_id = problem.problem_id[0]
                self.contests.append([])
            self.contests[-1].append(problem)

        self.size_y = TOP_BOTTOM_SPACE*2 +\
            len(self.contests) * (PROBLEM_SIZE_Y + PROBLEM_Y_INTERVAL) - PROBLEM_Y_INTERVAL
        self.size_x = PROBLEM_X_MIN_INTERVAL +\
            len(max(self.contests, key=lambda x: len(x))) * (PROBLEM_SIZE_X + PROBLEM_X_MIN_INTERVAL)

        self.image = drawer.Image((self.size_x, self.size_y), BACKGROUND_COLOR)

        self._locate_problems()
        self._locate_lines()

        self._draw_tree()

    def _locate_problems(self):
        self.problem_coords = dict()
        self.problems_and_coords = []
        current_y = TOP_BOTTOM_SPACE
        for contest_index, contest in enumerate(self.contests):
            x_interval = (self.size_x - len(contest) * PROBLEM_SIZE_X) / (len(contest) + 1)
            for problem_index, problem in enumerate(contest):
                problem_x = int((x_interval + PROBLEM_SIZE_X) * (problem_index + 1) - PROBLEM_SIZE_X)
                self.problem_coords[problem] = (problem_x, current_y)
                self.problems_and_coords.append((problem, (problem_x, current_y)))
            current_y += PROBLEM_SIZE_Y + PROBLEM_Y_INTERVAL

    def _locate_lines(self):
        self.lines = []
        force_field = [[0.0, 0.0] for j in range(self.size_x * self.size_y)]
        force_field_last_added = [-1 for j in range(self.size_x * self.size_y)]
        for problem_2 in self.problems:
            problem_1 = self.tree.get_previous_problem(problem_2)
            if problem_1 is None:
                continue
            curr_x, curr_y = tuple(map(float, self.problem_coords[problem_1]))
            problem_2_coords = tuple(map(float, self.problem_coords[problem_2]))
            destination = (problem_2_coords[0] + PROBLEM_SIZE_X / 2, problem_2_coords[1] + PROBLEM_SIZE_Y / 2)
            curr_x += PROBLEM_SIZE_X / 2
            curr_y += PROBLEM_SIZE_Y / 2
            curr_vx, curr_vy = 0.0, 0.0
            self.lines.append([])
            steps = 0
            while True:
                steps += 1
                if steps == 3000:
                    print("Failed to locate line")
                    break
                speed_sqr = _vector_length_sqr((curr_vx, curr_vy))
                if speed_sqr > LOCATE_LINES_MAX_SPEED_SQR:
                    speed = speed_sqr ** 0.5
                    curr_vx *= LOCATE_LINES_MAX_SPEED / speed
                    curr_vy *= LOCATE_LINES_MAX_SPEED / speed
                new_line_point = (int(curr_x), int(curr_y))
                if len(self.lines[-1]) == 0 or new_line_point != self.lines[-1][-1]:
                    self.lines[-1].append(new_line_point)
                curr_x += curr_vx
                curr_y += curr_vy
                if _is_point_in_rectangle((curr_x, curr_y), problem_2_coords, (PROBLEM_SIZE_X, PROBLEM_SIZE_Y)):
                    break
                for problem, problem_coords in self.problems_and_coords:
                    if problem in (problem_1, problem_2):
                        continue
                    distance_sqr = _point_rectangle_distance_sqr((curr_x, curr_y), problem_coords,
                                                                 (PROBLEM_SIZE_X, PROBLEM_SIZE_Y))
                    inverse_distance_sqr = 1.0 / distance_sqr
                    direction = _normalize((problem_coords[0] - curr_x, problem_coords[1] - curr_y))
                    curr_vx += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[0]
                    curr_vy += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[1]
                destination_direction = _normalize((destination[0] - curr_x, destination[1] - curr_y))
                curr_vx += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[0]
                curr_vy += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[1]
                curr_x_int = int(curr_x)
                curr_y_int = int(curr_y)
                if 0 <= curr_x_int < self.size_x and 0 <= curr_y_int < self.size_y:
                    curr_vx += force_field[curr_x_int * self.size_y + curr_y_int][0]
                    curr_vy += force_field[curr_x_int * self.size_y + curr_y_int][1]
            self.lines[-1].append((int(curr_x), int(curr_y)))

            point_1 = (None, None)
            for point_2 in self.lines[-1]:
                if point_1[0] is not None:
                    line_a = point_2[1] - point_1[1]
                    line_b = point_1[0] - point_2[0]
                    line_a, line_b = _normalize((line_a, line_b))
                    line_c = (point_1[0] * line_a + point_1[1] * line_b) * -1
                    for cx in range(min(point_1[0], point_2[0]) - LOCATE_LINES_LINE_FORCE_DISTANCE,
                                    max(point_1[0], point_2[0]) + LOCATE_LINES_LINE_FORCE_DISTANCE):
                        if cx < 0 or cx >= self.size_x:
                            continue
                        for cy in range(min(point_1[1], point_2[1]) - LOCATE_LINES_LINE_FORCE_DISTANCE,
                                        max(point_1[1], point_2[1]) + LOCATE_LINES_LINE_FORCE_DISTANCE):
                            if cy < 0 or cy >= self.size_y:
                                continue
                            cxcy = cx * self.size_y + cy
                            if force_field_last_added[cxcy] == len(self.lines):
                                continue
                            distance = line_a * cx + line_b * cy + line_c
                            if math.fabs(distance) <= LOCATE_LINES_LINE_FORCE_DISTANCE:
                                force_field_last_added[cxcy] = len(self.lines)
                                if distance >= 0.0:
                                    force_field[cxcy][0] += line_a * LOCATE_LINES_LINE_CONSTANT_FORCE
                                    force_field[cxcy][1] += line_b * LOCATE_LINES_LINE_CONSTANT_FORCE
                                else:
                                    force_field[cxcy][0] -= line_a * LOCATE_LINES_LINE_CONSTANT_FORCE
                                    force_field[cxcy][1] -= line_b * LOCATE_LINES_LINE_CONSTANT_FORCE
                point_1 = point_2


    def _draw_problem(self, problem, coords):
        self.image.draw_rectangle(coords, (PROBLEM_SIZE_X, PROBLEM_SIZE_Y), PROBLEM_BORDER_THICKNESS,
                                  PROBLEM_BORDER_COLOR, PROBLEM_FILL_COLOR)

    def _draw_tree(self):
        for line in self.lines:
            self.image.draw_line_strip(line, TREE_LINE_THICKNESS, TREE_LINE_COLOR)
        for problem, problem_coords in self.problems_and_coords:
            self._draw_problem(problem, problem_coords)

    def save_image_to_file(self, filename):
        self.image.save_png(filename)

