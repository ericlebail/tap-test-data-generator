import itertools
from collections import namedtuple

from allpairspy import AllPairs


def compute_value_pairs(value_lists, pair_generation_mode):
    pair_values = []
    keys = value_lists.keys()
    vals = value_lists.values()
    Pairs = namedtuple("Pairs", keys)
    if 'all_combinations' == pair_generation_mode:
        # create Pairs using cartesian product of value lists
        pair_values = cartesian_product(Pairs, keys, vals)
    elif 'every_value_at_least_once' == pair_generation_mode:
        # create Pairs until every value is used at least once
        pair_values = every_value_once(Pairs, keys, vals)
    else:
        # computing pairwise Pairs using lib
        pair_values = AllPairs(value_lists)
    return pair_values


def cartesian_product(Pairs, keys, vals):
    pair_values = []
    for instance in itertools.product(*vals):
        pair_values.append(Pairs(**dict(zip(keys, instance))))
    return pair_values


def every_value_once(Pairs, keys, vals):
    pair_values = []
    # first get the longest list
    max_length = 0
    for values in vals:
        if len(values) > max_length:
            max_length = len(values)
    # create a new list of list by cycling for the short ones
    new_vals = []
    for values in vals:
        if len(values) < max_length:
            new_vals.append(itertools.cycle(values))
        else:
            new_vals.append(iter(values))
    # create the Pairs
    index = 0
    while index < max_length:
        index += 1
        current_values = []
        for new_values in new_vals:
            current_values.append(next(new_values))
        current_dict = dict(zip(keys, current_values))
        pair_values.append(Pairs(**current_dict))
    return pair_values
