
# intended answers:

###############
# Also see two really cool solutions from tomityrrell: 
# The first uses a custom formatter, and the other uses the PrettyPrint module, which handles recursive structures quite well by default.
# https://github.com/tomityrrell/novice_nuggets/blob/main/novice_nuggets/novice_nuggets_2_solution.py
# Thanks Tomi!

###############
# altv 1  [could be called 'replace_keys']

def replace_keys(dictt, keys_to_replace, new_value):
    return {k: (new_value if k in keys_to_replace else v) for k, v in dictt.items()}
    # k in keys_to_replace ? new_value : v

def shrink_for_logging_1(data):
    log.info('data=%s', replace_keys(data, ['content'], 'too big to log'))

###############
# altv 2  [could be called 'loggable_dict']

# generators are a less verbose way to create a contextmanager than
# creating a class that defines __enter__ and __exit__ methods.

from contextlib import contextmanager
@contextmanager
def loggable_dict(dictt, keys_to_replace, new_value):
    temp_data = {k: (new_value if k in keys_to_replace else v) for k, v in dictt.items()}
    try:
        yield temp_data
    finally:
        del temp_data

def shrink_for_logging_2(data):
    with loggable_dict(data, ['content'], 'too big to log') as temp_data:
        log.info('data=%s', temp_data)

###############
# what if the keys_to_replace could be at any depth?

#######
# recursive solution

# dict.copy does a shallow copy--we need deepcopy here.
from copy import deepcopy

def replace_keys_recursive(mapping, keys_to_replace, new_value):
    # assumes values are either primitive or dict, not list.
    result = copy.deepcopy(mapping)
    try:
        for key, val in result.items():
            if key in keys_to_replace:
                result[key] = new_value
            else:
                replace_keys_recursive(val, keys_to_replace, new_value)
    except AttributeError:
        pass

    return result


def shrink_for_logging_3(data):
    log.info('data=%s', replace_keys_recursive(data, ['content'], 'too big to log'))


#######
# mike's iterative solution

from copy import deepcopy
from collections import deque
from typing import Mapping, Iterable

def replace_keys_iterative(mapping: Mapping, keys_to_replace: Iterable[str]) -> Mapping:
    result = copy.deepcopy(mapping)
    queue = deque()
    queue.appendleft(result)
    while queue:
        item = queue.pop()
        if isinstance(item, dict):
            for key, value in item.items():
                if key in keys_to_replace:
                    item[key] = "too big to log"
                elif isinstance(value, dict):
                    queue.appendleft(value)
    return result


def shrink_for_logging_4(data):
    log.info('data=%s', replace_keys_iterative(data, ['content'], 'too big to log'))


import logging
log = logging.getLogger()

def main():

    class LogCatcher(logging.StreamHandler):
        # handler to collect log output for testing.
        def emit(self, record):
            msg = record.getMessage()
            print('LogCatcher emitting:', msg)
            # check 1: ensure dict content is abbreviated.
            assert "'content': 'too big to log'" in msg

    log.setLevel('INFO')
    log.addHandler(LogCatcher())

    flat_solutions = [shrink_for_logging_1, shrink_for_logging_2]
    deep_solutions = [shrink_for_logging_3, shrink_for_logging_4]
    all_solutions = flat_solutions + deep_solutions

    for shrink_for_logging in all_solutions:
        flat_data = {1: 2, 'a': 'b', 'content': 'abc' * 10_000}
        flat_data_to_shrink = deepcopy(flat_data)

        shrink_for_logging(flat_data_to_shrink)

        # check 2: ensure dict has not changed
        assert flat_data_to_shrink == flat_data, 'data should not have changed but did'

        if shrink_for_logging in deep_solutions:
            deep_data = {1: 2, 'a': 'b', 'extra_level': {'content': 'abc' * int(1e4)}}
            deep_data_to_shrink = deepcopy(deep_data)
            shrink_for_logging(deep_data_to_shrink)
            assert deep_data_to_shrink == deep_data, 'data should not have changed but did'


if __name__ == '__main__': import sys; sys.exit(main())
