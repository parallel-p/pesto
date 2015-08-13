def locate_problems_and_texts(seasons):
    group_text = ('Arial', 25, 'black', 'center')
    day_text = ('Arial', 16, 'black', 'left')
    season_text = ('Arial', 22, 'black', 'center')

    day_height = 40
    day_name_width = 100
    group_name_height = 60
    problem_width = 30
    season_name_width = 250
    columns_spacing = 60

    column_width = [0] * 35
    row_height = [0] * len(seasons)
    for i, season in enumerate(seasons):
        row_height[i] = group_name_height + len(season.days) * day_height
        for group in season.groups:
            column_width[group.order] = max(column_width[group.order], group.max_len * problem_width)
    column_x = [season_name_width + day_name_width]
    for i in range(1, 35):
        column_x[i] = column_x[i - 1] + column_width[i - 1] + columns_spacing

    problems, texts = [], []
    y = 0
    for i, season in enumerate(seasons):
        texts.append((season.name, (season_name_width / 2, y + row_height[i] / 2)) + season_text)
        ty = y + group_name_height / 2
        for group in season.groups:
            tx = column_x[group.order] + column_width[group.order] / 2
            texts.append((group.name, (tx, ty)) + group_text)
        y += group_name_height
        for day in season.days:
            tx = season_name_width
            ty = y + day_height / 2
            texts.append((day.name, (tx, ty), day_text))
            for group in season.groups:
                for j, problem in enumerate(day.problems[group.name]):
                    tx = column_x[group.order] + (j + 0.5) * problem_width
                    problems.append((problem, (tx, ty)))
            y += day_height
