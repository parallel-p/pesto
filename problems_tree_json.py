import json


def save_tree(tree, contest_grouper):
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
    return json.dumps(result, indent=4)

