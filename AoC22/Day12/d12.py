#!/bin/python3

import sys


# check if a file name was passed as an argument
file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

# print the file name that will be used
print("Using file {}".format(file))


def bfs(maze, start, end):
    #initialise the queue with the start poistion and a scort of 0
    queue = [(start, 0)]
     # Initialize the set of visited positions
    visited = set()
     # Initialize the best score with a large value
    best = 100000

    
     # Loop until the queue is empty
    while len(queue) > 0:
        # Pop the first position from the queue
        (curr, score) = queue.pop(0)
        
        # If the current position is the end position, update the best score
        # if the current score is lower than the best score, and continue to the
        # next iteration

        if curr == end:
            if score < best:
                best = score
            continue

        if curr in visited:
            continue

        visited.add(curr)

        up = (curr[0], curr[1] - 1)
        down = (curr[0], curr[1] + 1)
        left = (curr[0] - 1, curr[1])
        right = (curr[0] + 1, curr[1])

        for dir in [up, down, left, right]:
            if dir[0] >= 0 and dir[0] < len(maze[0]) and dir[1] >= 0 and dir[1] < len(maze):
                current_height = maze[curr[1]][curr[0]]

                if current_height == "S":
                    current_height = "a"

                new_height = maze[dir[1]][dir[0]]

                if new_height == "E":
                    new_height = "z"

                if ord(current_height) + 1 >= ord(new_height):
                    queue.append((dir, score + 1))

    return best


with open(file) as f:
    maze = [[c for c in line.strip()] for line in f.readlines()]

    start = (0, 0)
    end = (0, 0)
    a_positions = []
    for (y, r) in enumerate(maze):
        for (x, cell) in enumerate(r):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
            elif cell == "a":
                a_positions.append((x, y))

    print("First part: {}".format(bfs(maze, start, end)))
    print("Second part: {}".format(min([bfs(maze, a, end) for a in a_positions])))
