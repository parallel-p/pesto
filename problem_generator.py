import config
import model
import md5_hasher


def problem_generator(contest_dirs):
    config_parser = config.Config()
    for contest_dir in contest_dirs:
        config_parser.parse(contest_dir)
        cases = config_parser.get_filenames()
        current_problem_cases = []
        current_problem_name = ""
        for case in cases:
            problem_name = case[0].split("/")[-2]
            if current_problem_name != problem_name:
                if current_problem_name != "":
                    yield model.Problem(config_parser.get_problem_id(current_problem_name),
                                        current_problem_name,
                                        current_problem_cases)
                current_problem_name = problem_name
                current_problem_cases = []
            current_problem_cases.append(md5_hasher.get_hash(case[0], case[1]))
        if current_problem_name != "":
            yield model.Problem(config_parser.get_problem_id(current_problem_name),
                                current_problem_name,
                                current_problem_cases)
