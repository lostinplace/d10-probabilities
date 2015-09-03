__author__ = 'cwheeler'

import itertools
import functools

default_probabilities = {
    'S': 0.4, 
    'F':0.4, 
    'O': 0.1, 
    'T':0.1
}


def eval_roll(roll, spec_counts=False, probabilities=default_probabilities):

    key = ''.join(roll)

    successes = roll.count('S')
    failures = roll.count('F')
    ones = roll.count('O')
    tens = roll.count('T')

    p_success = (probabilities['S'] ** successes)
    p_failures = (probabilities['F'] ** failures)
    p_ones = (probabilities['O'] ** ones)
    p_tens = (probabilities['T'] ** tens)

    p_roll = p_success * p_failures * p_ones * p_tens

    score = successes + (tens * (2 if spec_counts else 1))
    if score == 0 and ones > 0:
        score = -1
    else:
        score = 0 if ones > score else score - ones

    return key, {'score': score, 'probability': round(p_roll,10)}


def determine_probabilities(target_number):
    success_positions = 10 - target_number
    failure_positions = 10 - success_positions - 2
    return {'S': success_positions / 10, 'F': failure_positions / 10, 'O': 0.1, 'T': 0.1}


def get_rolls(number_of_dice):
    return itertools.product('SFOT', repeat=number_of_dice)


def build_probability_map(number_of_dice=3, target_number=6, spec_counts=False):
    probabilities = determine_probabilities(target_number)
    rolls = get_rolls(number_of_dice)
    roll_evaluations = map(lambda a_roll: eval_roll(a_roll, spec_counts, probabilities), rolls)
    probability_map = dict(roll_evaluations)
    return probability_map


def build_score_probability_map(probability_map):
    score_map = map(lambda k: (probability_map[k]['score'], probability_map[k]['probability']), probability_map)
    sList = sorted(score_map)

    keyfunc = lambda v: v[0]

    for k, g in itertools.groupby(sList, keyfunc):
        vals = map(lambda v: v[1], g)
        aSum = functools.reduce(lambda a,b: round(a+b, 10), vals)
        yield k, aSum

        
def get_score_probability_map(target, number_of_dice, spec_counts=False):
    pm = build_probability_map( number_of_dice, target, spec_counts)
    spm = build_score_probability_map(pm)
    return spm


def get_cumulative_probability_for_key(dictionary, index, operator = 'gte'):
    applicable_keys = filter(lambda v:  v>=index if operator == 'gte' else v<=index, dictionary.keys())
    cumulative_probability = sum([dictionary[x] for x in applicable_keys])
    return cumulative_probability


def get_cumulative_probability_for_dictionary(a_dictionary):
    bins = sorted(a_dictionary.keys())
    vals = list(map(lambda v: get_cumulative_probability_for_key(a_dictionary,v),bins))
    return zip(bins,vals)
