import math

import logging

import drawer


BACKGROUND_COLOR = "black"

PROBLEM_RADIUS = 10
PROBLEM_DIAMETER = PROBLEM_RADIUS * 2
PROBLEM_FILL_COLOR = '#FF9347'
PROBLEM_BORDER_COLOR = '#FF9347'
PROBLEM_BORDER_THICKNESS = 2

LINE_THICKNESS = 2

LOCATE_LINES_MAX_SPEED = 3.0
LOCATE_LINES_MAX_SPEED_SQR = LOCATE_LINES_MAX_SPEED ** 2
LOCATE_LINES_PROBLEMS_FORCE = -150.0
LOCATE_LINES_DESTINATION_CONSTANT_FORCE = 2.0
LOCATE_LINES_MAX_ITERATIONS = 40000
CHUNK_SIZE = 200

LOCATE_LINES_LINE_CONSTANT_FORCE = 0.25
LOCATE_LINES_LINE_FORCE_DISTANCE = 10

LINE_COLOR_SAME = (0, 255, 0)
LINE_COLOR_MIN = (255, 0, 0)
LINE_COLOR_MAX = (255, 255, 0)
MIN_SIMILARITY = 0.5

LINE_ARROW_ANGLE = math.pi / 7.0
LINE_ARROW_LENGTH = 10.0

SEASON_NAME_WIDTH = 200
GROUP_NAME_HEIGHT = 30
DAY_NAME_HEIGHT = 40
DAY_NAME_WIDTH = 70
DAY_SPACING = 30
PROBLEM_WIDTH = 40
PROBLEM_HEIGHT = 30
GROUPS_SPACING = 40
END_SPACE = 50
MAX_GROUP_COUNT = 15
SEASON_SPACING = 150


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
        group_text = ('fonts/Arial.ttf', 25, 'white', 'left')
        day_text = ('fonts/Arial.ttf', 16, 'white', 'left')
        season_text = ('fonts/Arial.ttf', 22, 'white', 'center')

        column_width = [0] * MAX_GROUP_COUNT
        for season in self.seasons:
            for group in season.groups:
                problems_width = sum([max(len(day.problems) * PROBLEM_WIDTH, DAY_NAME_WIDTH) for day in group.days])
                group_width = problems_width + (len(group.days) - 1) * DAY_SPACING
                column_width[group.order] = max(column_width[group.order], group_width)
        column_x = [SEASON_NAME_WIDTH]
        for i in range(1, MAX_GROUP_COUNT):
            column_x.append(column_x[i - 1] + column_width[i - 1])
            if column_width[i - 1] > 0:
                column_x[i] += GROUPS_SPACING

        group_ty = GROUP_NAME_HEIGHT / 2
        day_ty = GROUP_NAME_HEIGHT + DAY_NAME_HEIGHT / 2
        problem_ty = GROUP_NAME_HEIGHT + DAY_NAME_HEIGHT + PROBLEM_HEIGHT / 2
        row_height = GROUP_NAME_HEIGHT + DAY_NAME_HEIGHT + PROBLEM_HEIGHT
        text_space = PROBLEM_WIDTH * 0.3

        y = 0
        self.size_x, self.size_y = 0, 0

        for season in self.seasons:
            txt = '{}.{}'.format(season.name[0], season.name[1])
            self.texts.append((txt, (SEASON_NAME_WIDTH / 2, y + row_height / 2)) + season_text)
            for group in season.groups:
                tx = column_x[group.order]
                self.texts.append((group.name, (tx + text_space, y + group_ty)) + group_text)
                for day in group.days:
                    txt = 'Day {}'.format(day.name) if day.name.isdigit() else day.name
                    self.texts.append((txt, (tx + text_space, y + day_ty)) + day_text)
                    cx = tx + DAY_NAME_WIDTH
                    for problem in day.problems:
                        px, py = tx + PROBLEM_WIDTH / 2, y + problem_ty
                        self.problems_and_coords.append((problem, (px, py)))
                        self.problem_coords[problem] = (px, py)
                        self.size_x = max(self.size_x, int(px) + END_SPACE)
                        self.size_y = max(self.size_y, int(py) + END_SPACE)
                        tx += PROBLEM_WIDTH
                    tx = max(tx, cx) + DAY_SPACING
            y += row_height + SEASON_SPACING

    def _create_seasons(self):
        seasons_dict, groups_dict, days_dict = dict(), dict(), dict()
        for problem in self.problems:
            contest_id = problem.problem_id[0]
            group_name = self.contests_grouper.get_contest_parallel_by_id(contest_id)
            season_name = self.contests_grouper.get_contest_season_by_id(contest_id)
            day_name = self.contests_grouper.get_contest_day_by_id(contest_id)
            year = self.contests_grouper.get_contest_year_by_id(contest_id)
            season_name = (str(year), season_name)
            if '' in [group_name, season_name]:
                continue
            season_key = season_name
            if season_key not in seasons_dict:
                self.seasons.append(Season(season_name))
                seasons_dict[season_key] = self.seasons[-1]
            season = seasons_dict[season_key]
            group_key = (season_key, group_name)
            if group_key not in groups_dict:
                season.groups.append(Group(group_name))
                groups_dict[group_key] = season.groups[-1]
            group = groups_dict[group_key]
            day_key = (group_key, day_name)
            if day_key not in days_dict:
                group.days.append(Day(day_name))
                days_dict[day_key] = group.days[-1]
            day = days_dict[day_key]
            day.problems.append(problem)
        for season in self.seasons:
            for group in season.groups:
                for day in group.days:
                    day.problems.sort(key=lambda p: p.problem_id[1])
                group.days.sort(key=lambda d: d.problems[0].problem_id[0])
            season.groups.sort(key=lambda g: g.order)
        self.seasons.sort(key=lambda s: s.get_order())

    def _get_line_color(self, problem):
        parent, similarity, same, added, removed = self.tree.get_relation_to_parent(problem)
        if removed == 0 and added == 0:
            return LINE_COLOR_SAME
        color_k = (similarity - MIN_SIMILARITY) / (1.0 - MIN_SIMILARITY)
        return (int(LINE_COLOR_MIN[0] + color_k * (LINE_COLOR_MAX[0] - LINE_COLOR_MIN[0])),
                int(LINE_COLOR_MIN[1] + color_k * (LINE_COLOR_MAX[1] - LINE_COLOR_MIN[1])),
                int(LINE_COLOR_MIN[2] + color_k * (LINE_COLOR_MAX[2] - LINE_COLOR_MIN[2])))

    def _locate_lines(self):
        self.lines, self.arrows, self.lines_colors = [], [], []

        chunks_x, chunks_y = (self.size_x + CHUNK_SIZE - 1) // CHUNK_SIZE, \
                             (self.size_y + CHUNK_SIZE - 1) // CHUNK_SIZE
        chunks = [[] for i in range(chunks_x * chunks_y)]
        for problem_and_coords in self.problems_and_coords:
            coords = problem_and_coords[1]
            chunk_x = int(coords[0]) // CHUNK_SIZE
            chunk_y = int(coords[1]) // CHUNK_SIZE
            chunks[chunk_x * chunks_y + chunk_y].append(problem_and_coords)

        fails = 0
        for problem_2 in self.problems:
            if problem_2 not in self.problem_coords:
                logging.warning('wtf {} {}'.format(problem_2.problem_id, problem_2.name))  # idk what it means
                continue
            problem_1 = self.tree.get_previous_problem(problem_2)
            if problem_1 is None or problem_1 not in self.problem_coords:
                if problem_1 is not None:
                    logging.warning('wtf {} {}'.format(problem_1.problem_id, problem_1.name))  # same here
                continue
            curr_x, curr_y = tuple(map(lambda x: float(x), self.problem_coords[problem_1]))
            destination = tuple(map(float, self.problem_coords[problem_2]))
            curr_vx, curr_vy = 0.0, 3.0
            self.lines.append([])
            self.lines_colors.append(self._get_line_color(problem_2))

            steps = 0
            while True:
                steps += 1
                if steps == LOCATE_LINES_MAX_ITERATIONS:
                    logging.warning("Failed to locate line {}".format(len(self.lines) - 1))
                    fails += 1
                    self.lines[-1] = []
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
                    logging.info("Line {} located".format(len(self.lines) - 1))
                    break
                chunk_x = int(curr_x) // CHUNK_SIZE
                chunk_y = int(curr_y) // CHUNK_SIZE
                for curr_chunk_x in range(chunk_x - 1, chunk_x + 2):
                    for curr_chunk_y in range(chunk_y - 1, chunk_y + 2):
                        if not (0 <= curr_chunk_x < chunks_x and 0 <= curr_chunk_y < chunks_y):
                            continue
                        for problem, problem_coords in chunks[curr_chunk_x * chunks_y + curr_chunk_y]:
                            if problem in (problem_1, problem_2):
                                continue
                            distance_sqr = (
                                           _distance_sqr((curr_x, curr_y), problem_coords) ** 0.5 - PROBLEM_RADIUS) ** 2
                            inverse_distance_sqr = 1.0 / distance_sqr
                            direction = _normalize((problem_coords[0] - curr_x, problem_coords[1] - curr_y))
                            curr_vx += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[0]
                            curr_vy += LOCATE_LINES_PROBLEMS_FORCE * inverse_distance_sqr * direction[1]
                destination_direction = _normalize((destination[0] - curr_x, destination[1] - curr_y))
                curr_vx += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[0]
                curr_vy += LOCATE_LINES_DESTINATION_CONSTANT_FORCE * destination_direction[1]

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
        logging.info("Lines located, {} fails".format(fails))

    def _draw_problem(self, problem, coords):
        self.image.draw_circle(coords, PROBLEM_RADIUS, PROBLEM_BORDER_THICKNESS,
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
    def __init__(self, name):
        self.name = name
        self.groups = []

    def get_order(self):
        pos = {'июль': 0, 'август': 1, 'зима': 2}
        year = int(self.name[0])
        name = self.name[1].lower()
        order = pos[name] if name in pos else 3
        return year, order


class Group:
    def __init__(self, name):
        self.name = name
        self.order = self._get_order()
        self.days = []

    def _get_order(self):
        order_dict = {'A': 0, 'A+': 0,
                      'A\'': 1, 'A\'+': 1,
                      'A0': 2,
                      'AA': 3,
                      'AS': 4,
                      'AY': 5,
                      'B': 6, 'B+': 6,
                      'B\'': 7, 'B\'+': 7,
                      'C': 8, 'Ccpp': 8, 'C+': 8, 'Ccpp+': 8,
                      'Cpy': 9, 'Cpy+': 9,
                      'C\'': 10, 'C\'+': 10,
                      'D': 11,
                      'olymp': 12}
        if self.name in order_dict:
            return order_dict[self.name]
        else:
            return 13


class Day:
    def __init__(self, name):
        self.name = name
        self.problems = []
