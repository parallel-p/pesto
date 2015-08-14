import drawer
import math
import sys


BACKGROUND_COLOR = "white"

PROBLEM_RADIUS = 10
PROBLEM_DIAMETER = PROBLEM_RADIUS * 2
PROBLEM_FILL_COLOR = "yellow"
PROBLEM_BORDER_COLOR = "black"
PROBLEM_BORDER_THICKNESS = 2

LINE_THICKNESS = 1

LOCATE_LINES_MAX_SPEED = 3.0
LOCATE_LINES_MAX_SPEED_SQR = LOCATE_LINES_MAX_SPEED ** 2
LOCATE_LINES_PROBLEMS_FORCE = -150.0
LOCATE_LINES_DESTINATION_CONSTANT_FORCE = 2.0
LOCATE_LINES_MAX_ITERATIONS = 3000

LOCATE_LINES_LINE_CONSTANT_FORCE = 1.0
LOCATE_LINES_LINE_FORCE_DISTANCE = 20

LINE_COLOR_SAME = (0, 255, 0)
LINE_COLOR_MIN = (255, 0, 0)
LINE_COLOR_MAX = (255, 255, 0)
MIN_SIMILARITY = 0.5

LINE_ARROW_ANGLE = math.pi / 30.0
LINE_ARROW_LENGTH = 15.0

DAY_HEIGHT = 40
DAY_NAME_WIDTH = 100
GROUP_NAME_HEIGHT = 60
PROBLEM_WIDTH = 50
SEASON_NAME_WIDTH = 250
COLUMNS_SPACING = 60
END_SPACE = 100
MAX_GROUP_COUNT = 35


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


def _vector_rotate(v, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    return (v[0] * c - v[1] * s, v[1] * c + v[0] * s)


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


class TreeDrawer:
    def __init__(self, tree, contests_grouper):
        self.tree = tree
        self.contests_grouper = contests_grouper
        self.problems = self.tree.get_problems()
        self.seasons = []
        self._create_seasons()

        self.problem_coords = dict()
        self.problems_and_coords = []
        self.texts = []
        self._locate_problems_and_texts()
        self.lines, self.arrows = [], []
        self._locate_lines()

        self.image = drawer.Image((self.size_x, self.size_y), BACKGROUND_COLOR)
        self._draw_tree()

    def _locate_problems_and_texts(self):
        group_text = ('fonts/Arial.ttf', 25, 'black', 'center')
        day_text = ('fonts/Arial.ttf', 16, 'black', 'left')
        season_text = ('fonts/Arial.ttf', 22, 'black', 'center')

        column_width = [0] * MAX_GROUP_COUNT
        row_height = [0] * len(self.seasons)
        for i, season in enumerate(self.seasons):
            row_height[i] = GROUP_NAME_HEIGHT + len(season.days) * DAY_HEIGHT
            for group in season.groups:
                column_width[group.order] = max(column_width[group.order], group.max_len * PROBLEM_WIDTH)
        column_x = [SEASON_NAME_WIDTH + DAY_NAME_WIDTH]
        for i in range(1, MAX_GROUP_COUNT):
            column_x.append(column_x[i - 1] + column_width[i - 1])
            if column_x[i - 1] > 0:
                column_x[i] += COLUMNS_SPACING

        y = 0
        self.size_x, self.size_y = 0, 0
        for i, season in enumerate(self.seasons):
            self.texts.append((season.name, (SEASON_NAME_WIDTH / 2, y + row_height[i] / 2)) + season_text)
            ty = y + GROUP_NAME_HEIGHT / 2
            for group in season.groups:
                tx = column_x[group.order] + column_width[group.order] / 2
                self.texts.append((group.name, (tx, ty)) + group_text)
            y += GROUP_NAME_HEIGHT
            for day in season.days:
                tx = SEASON_NAME_WIDTH
                ty = y + DAY_HEIGHT / 2
                self.texts.append((day.name, (tx, ty)) + day_text)
                for group in season.groups:
                    for j, problem in enumerate(day.problems[group.name]):
                        tx = column_x[group.order] + (j + 0.5) * PROBLEM_WIDTH
                        self.problems_and_coords.append((problem, (tx, ty)))
                        self.problem_coords[problem] = (tx, ty)
                        self.size_x = max(self.size_x, int(tx + END_SPACE))
                        self.size_y = max(self.size_y, int(ty + END_SPACE))
                y += DAY_HEIGHT

    def _create_seasons(self):
        seasons_dict = dict()
        for problem in self.problems:
            contest_id = problem.problem_id[0]

            group = self.contests_grouper.get_contest_parallel_by_id(contest_id)
            season_name = self.contests_grouper.get_contest_season_by_id(contest_id)
            day = self.contests_grouper.get_contest_day_by_id(contest_id)
            year = self.contests_grouper.get_contest_year_by_id(contest_id)

            if '' in [group, season_name]:
                continue

            key = str(year) + season_name

            if key not in seasons_dict:
                seasons_dict[key] = Season(season_name, year)
            seasons_dict[key].add_day_and_problem(problem, day, group, contest_id)
        for key in seasons_dict:
            seasons_dict[key].create_group_list()
            seasons_dict[key].create_days_list()
            seasons_dict[key].count_max_len()
            self.seasons.append(seasons_dict[key])
        self.seasons.sort(key=lambda x: x.order)

    def _get_line_color(self, problem):
        parent, similarity, same, added, removed = self.tree.get_relation_to_parent(problem)
        if removed == 0 and added == 0:
            return LINE_COLOR_SAME
        color_k = (similarity - MIN_SIMILARITY) / (1.0 - MIN_SIMILARITY)
        return (int(LINE_COLOR_MIN[0] + color_k * (LINE_COLOR_MAX[0] - LINE_COLOR_MIN[0])),
                int(LINE_COLOR_MIN[1] + color_k * (LINE_COLOR_MAX[1] - LINE_COLOR_MIN[1])),
                int(LINE_COLOR_MIN[2] + color_k * (LINE_COLOR_MAX[2] - LINE_COLOR_MIN[2])))

    def _locate_lines(self):
        self.lines = []
        self.arrows = []
        self.lines_colors = []
        #force_field = [[0.0, 0.0] for j in range(self.size_x * self.size_y)]
        #force_field_last_added = [-1 for j in range(self.size_x * self.size_y)]
        for problem_2 in self.problems:
            problem_1 = self.tree.get_previous_problem(problem_2)
            if problem_1 is None:
                continue
            curr_x, curr_y = tuple(map(float, self.problem_coords[problem_1]))
            destination = tuple(map(float, self.problem_coords[problem_2]))
            curr_vx, curr_vy = 0.0, 0.0
            self.lines.append([])
            self.lines_colors.append(self._get_line_color(problem_2))
            steps = 0
            while True:
                steps += 1
                if steps == LOCATE_LINES_MAX_ITERATIONS:
                    print("Failed to locate line", len(self.lines) - 1, file=sys.stderr)
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
                if _distance_sqr((curr_x, curr_y), destination) <= PROBLEM_RADIUS ** 2:
                    print("Line", len(self.lines) - 1, "located", file=sys.stderr)
                    break
                for problem, problem_coords in self.problems_and_coords:
                    if problem in (problem_1, problem_2):
                        continue
                    distance_sqr = (_distance_sqr((curr_x, curr_y), problem_coords) ** 0.5 - PROBLEM_RADIUS) ** 2
                    inverse_distance_sqr = 1.0 / distance_sqr
                    direction = _normalize((problem_coords[0] - curr_x, problem_coords[1] - curr_y))
                    curr_vx += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[0]
                    curr_vy += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[1]
                destination_direction = _normalize((destination[0] - curr_x, destination[1] - curr_y))
                curr_vx += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[0]
                curr_vy += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[1]
                curr_x_int = int(curr_x)
                curr_y_int = int(curr_y)
                #if 0 <= curr_x_int < self.size_x and 0 <= curr_y_int < self.size_y:
                #    curr_vx += force_field[curr_x_int * self.size_y + curr_y_int][0]
                #    curr_vy += force_field[curr_x_int * self.size_y + curr_y_int][1]
            self.lines[-1].append((int(curr_x), int(curr_y)))

            """point_1 = (None, None)
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
                point_1 = point_2"""

            self.arrows.append([])
            if len(self.lines[-1]) > 1:
                point_1 = self.lines[-1][-2]
                point_2 = self.lines[-1][-1]
                bs_l, bs_r = 0.0, 1.0
                while bs_r - bs_l > 0.001:
                    bs_mid = (bs_l + bs_r) * 0.5
                    point_3 = (point_1[0] + bs_mid * (point_2[0] - point_1[0]),
                               point_1[1] + bs_mid * (point_2[1] - point_1[1]))
                    if _distance_sqr(point_3, destination) < PROBLEM_RADIUS ** 2:
                        bs_r = bs_mid
                    else:
                        bs_l = bs_mid
                point_3 = (point_1[0] + bs_l * (point_2[0] - point_1[0]),
                           point_1[1] + bs_l * (point_2[1] - point_1[1]))
                arrow_vector = _normalize((point_1[0] - point_2[0], point_1[1] - point_2[1]))
                arrow_vector = (arrow_vector[0] * LINE_ARROW_LENGTH, arrow_vector[1] * LINE_ARROW_LENGTH)
                arrow_vector_1 = _vector_rotate(arrow_vector, LINE_ARROW_ANGLE)
                self.arrows[-1].append((point_3[0] + arrow_vector_1[0], point_3[1] + arrow_vector_1[1]))
                self.arrows[-1].append(point_3)
                arrow_vector_2 = _vector_rotate(arrow_vector, -LINE_ARROW_ANGLE)
                self.arrows[-1].append((point_3[0] + arrow_vector_2[0], point_3[1] + arrow_vector_2[1]))

    def _draw_problem(self, problem, coords):
        self.image.draw_circle(coords, PROBLEM_RADIUS,  PROBLEM_BORDER_THICKNESS,
                               PROBLEM_BORDER_COLOR, PROBLEM_FILL_COLOR)

    def _draw_tree(self):
        for index in range(len(self.lines)):
            line = self.lines[index]
            arrow = self.arrows[index]
            line_color = self.lines_colors[index]
            self.image.draw_line_strip(line, LINE_THICKNESS, line_color)
            self.image.draw_line_strip(arrow, LINE_THICKNESS, line_color)
        for problem, problem_coords in self.problems_and_coords:
            self._draw_problem(problem, problem_coords)
        for text in self.texts:
            self.image.draw_text(*text)

    def save_image_to_file(self, filename):
        self.image.save_png(filename)


class Season:
    def __init__(self, name, year):
        #dict of days
        #day is dict of list with id of problem
        self.days_dict = dict()
        self.groups_dict = dict()

        self.groups = []
        self.days = []
        self.problems_cnt_by_day_by_group = dict()
        self.order = self._get_order(name, year)
        self.name = '{}.{}'.format(year, name)

    def add_day_and_problem(self, problem, day, group, contest_id):
        if day not in self.days_dict:
            self.days_dict[day] = Day(day, contest_id)
        self.days_dict[day].add_problem(problem, group)

        if group in self.problems_cnt_by_day_by_group:
            if day in self.problems_cnt_by_day_by_group[group]:
                self.problems_cnt_by_day_by_group[group][day] += 1
            else:
                self.problems_cnt_by_day_by_group[group][day] = 1
        else:
            self.problems_cnt_by_day_by_group[group] = {day:1}

        if group not in self.groups_dict:
            self.groups_dict[group] = Group(group)

    def count_max_len(self):
        for group in self.problems_cnt_by_day_by_group:
            max_res = 0
            for day in self.problems_cnt_by_day_by_group[group]:
                max_res = max(max_res, self.problems_cnt_by_day_by_group[group][day])
            self.groups_dict[group].max_len = max_res

    def create_days_list(self):
        for day in self.days_dict:
            self.days.append(self.days_dict[day])
        self.days.sort(key=lambda x: x.order)

    def create_group_list(self):
        for group in self.groups_dict:
            self.groups.append(self.groups_dict[group])
        self.groups.sort(key=lambda x: x.order)

    def _get_order(self, name, year):
        pos = {'июль' : 0, 'август' : 1, 'зима' : 2}
        order_2 = 3
        if name.lower() in pos:
            order_2 = pos[name.lower()]
        order_1 = int(year)
        return (order_1, order_2)


class Group:
    def __init__(self, group):
        self.max_len = 0
        self.name = group
        self.order = self._get_order(group)

    def _get_order(self, group):
        order_dict = {'A':0, 'A+':0,
                'A\'':1,
                'A0':2,
                'AA':3,
                'AS':4,
                'AY':5,
                'B':6,
                'B\'':7,
                'C':8, 'Ccpp':8, 'C+':8, 'Ccpp+':8,
                'C\'':9,
                'Cpy':10,
                'D':11,
                'olymp':12}
        if group in order_dict:
            return order_dict[group]
        else:
            return 13


class Day:
    def __init__(self, name, contest_id):
        self.name = name
        self.order = int(contest_id)
        self.problems = dict()

    def add_problem(self, problem, group):
        if group not in self.problems:
            self.problems[group] = []
        self.problems[group].append(problem)