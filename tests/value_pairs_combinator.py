from collections import namedtuple, OrderedDict

from tap_test_data_generator.value_pairs_combinator import cartesian_product, every_value_once, compute_value_pairs


def test_cartesian_product():
    # given
    list1 = [5, 10, 15, 20]
    list2 = ['bleu', 'red', 'green']
    list3 = [True, False]
    keys = ['number', 'color', 'checked']
    vals = [list1, list2, list3]
    Pairs = namedtuple("Pairs", keys)

    # when
    pair_values = cartesian_product(Pairs, keys, vals)

    # then
    assert pair_values is not None
    assert len(pair_values) is 24
    # test first item of the list
    pair = pair_values[0]
    assert getattr(pair, "number") is 5
    assert getattr(pair, "color") is "bleu"
    assert getattr(pair, "checked") is True


def test_every_value_once():
    # given
    list1 = [5, 10, 15, 20]
    list2 = ['bleu', 'red', 'green']
    list3 = [True, False]
    keys = ['number', 'color', 'checked']
    vals = [list1, list2, list3]
    Pairs = namedtuple("Pairs", keys)

    # when
    pair_values = every_value_once(Pairs, keys, vals)

    # then
    assert pair_values is not None
    assert len(pair_values) is 4
    # test first item of the list
    pair = pair_values[0]
    assert getattr(pair, "number") is 5
    assert getattr(pair, "color") is "bleu"
    assert getattr(pair, "checked") is True


def test_compute_value_pairs_every_value_at_least_once():
    # given
    list1 = [5, 10, 15, 20]
    list2 = ['bleu', 'red', 'green']
    list3 = [True, False]
    value_lists = OrderedDict({'number': list1, 'color': list2, 'checked': list3})

    # when
    pair_values = compute_value_pairs(value_lists, 'every_value_at_least_once')

    # then
    assert pair_values is not None
    item_number = 0
    for pair in pair_values:
        item_number += 1
        # test first item
        if 1 == item_number:
            assert getattr(pair, "number") is 5
            assert getattr(pair, "color") is "bleu"
            assert getattr(pair, "checked") is True
    # test item number
    assert item_number is 4


def test_compute_value_pairs_all_combinations():
    # given
    list1 = [5, 10, 15, 20]
    list2 = ['bleu', 'red', 'green']
    list3 = [True, False]
    value_lists = OrderedDict({'number': list1, 'color': list2, 'checked': list3})

    # when
    pair_values = compute_value_pairs(value_lists, 'all_combinations')

    # then
    assert pair_values is not None
    item_number = 0
    for pair in pair_values:
        item_number += 1
        # test first item
        if 1 == item_number:
            assert getattr(pair, "number") is 5
            assert getattr(pair, "color") is "bleu"
            assert getattr(pair, "checked") is True
    # test item number
    assert item_number is 24


def test_compute_value_pairs_default():
    # given
    list1 = [5, 10, 15, 20]
    list2 = ['bleu', 'red', 'green']
    list3 = [True, False]
    value_lists = OrderedDict({'number': list1, 'color': list2, 'checked': list3})

    # when
    pair_values = compute_value_pairs(value_lists, None)

    # then
    assert pair_values is not None
    item_number = 0
    for pair in pair_values:
        item_number += 1
        # test first item
        if 1 == item_number:
            assert getattr(pair, "number") is 5
            assert getattr(pair, "color") is "bleu"
            assert getattr(pair, "checked") is True
    # test item number
    assert item_number is 12
