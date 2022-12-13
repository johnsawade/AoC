#!/bin/python3

import sys
import json
import functools
# Read the name of the input file from the command line arguments
file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


def compare(left, right):
     """
    Compare two items in a JSON-formatted list and return 1 if the first item
    should be ranked higher than the second, -1 if the second item should be
    ranked higher than the first, or 0 if the items are equal.
    """
    # If both items are lists, compare the corresponding elements in each list
    if type(left) is list and type(right) is list:
        inner_len = min(len(left), len(right))
         # Compare the elements in each list until we find one that is not equal
        for l in range(inner_len):
            res = compare(left[l], right[l])
            if res == -1:
                return -1
            elif res == 1:
                return 1
         # If all the elements are equal, compare the lengths of the lists
        else:
            if len(left) > len(right):
                return -1
            elif len(left) < len(right):
                return 1
            else:
                return 0
    elif type(left) is list:
        right = [right]
        return compare(left, right)
    elif type(right) is list:
        left = [left]
        return compare(left, right)
    else:
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0


with open(file) as f:
    words = [json.loads(line.strip()) for line in f.readlines() if line.strip() != ""]
    index = 1
    score = 0

    for i in range(0, len(words), 2):
        a = i
        b = i + 1

        left = words[a]
        right = words[b]

        k = 0

        if compare(left, right) == 1:
            score += index

        index += 1

    print("Part one: {}".format(score))

    words.append([[2]])
    words.append([[6]])
    words.sort(key=functools.cmp_to_key(compare), reverse=True)
    print("Part two: {}".format((words.index([[2]]) + 1) * (words.index([[6]]) + 1)))
