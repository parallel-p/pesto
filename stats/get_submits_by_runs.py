def get_submits_by_runs(submits, runs_count, mode='eq'):
    if mode not in ['eq', 'gt', 'lt']:
        raise ValueError('Unknown mode: "{}"'.format(mode))
    if type(runs_count) != type(int()):
        raise ValueError('runs_count must be integer')
    ready_submits = []
    for submit in submits:
        if not hasattr(submit, 'runs'):
            raise TypeError('Incorrect submit passed.')
        if mode == 'eq' and len(submit.runs) == runs_count:
            ready_submits.append(submit)
        if mode == 'gt' and len(submit.runs) > runs_count:
            ready_submits.append(submit)
        if mode == 'lt' and len(submit.runs) < runs_count:
            ready_submits.append(submit)
    return ready_submits