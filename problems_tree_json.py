import json

import problems_tree
import stats.contests_grouper
import model


def save_tree(tree, contest_grouper, pretty=False):
    result = ([], [])
    problem_to_index = dict()
    for index, problem in enumerate(tree.get_problems()):
        problem_to_index[problem] = index
        relation_to_parent = tree.get_relation_to_parent(problem)
        if relation_to_parent is None:
            relation_to_parent = "None"
        else:
            relation_to_parent = (problem_to_index[relation_to_parent[0]], ) + relation_to_parent[1:]
        result[0].append({"id": problem.problem_id, "name": problem.name, "cases_count": len(problem.cases),
                          "parent": relation_to_parent})
    for contest_id in contest_grouper.contests:
        contest_data = contest_grouper.contests[contest_id]
        result[1].append({"id": contest_id, "data": (contest_data.year, contest_data.season,
                                                     contest_data.day, contest_data.parallel)})
    return json.dumps(result, indent=4) if pretty else json.dumps(result)


def load_tree(json_str):
    data = json.loads(json_str)
    tree = problems_tree.ProblemsTree([])
    tree.problems = []
    tree.problem_previous = dict()
    for problem in data[0]:
        tree.problems.append(model.Problem(problem["id"], '', problem["name"], (None, ) * problem["cases_count"]))
        relation_to_parent = problem["parent"]
        if relation_to_parent != "None":
            relation_to_parent = (tree.problems[int(relation_to_parent[0])], ) + tuple(relation_to_parent[1:])
            tree.problem_previous[tree.problems[-1]] = relation_to_parent
    contests_grouper = stats.contests_grouper.ContestsGrouper([])
    contests_grouper.contests = dict()
    for contest in data[1]:
        contests_grouper.contests[contest["id"]] = stats.contests_grouper._Contest(*contest["data"])
    return tree, contests_grouper
