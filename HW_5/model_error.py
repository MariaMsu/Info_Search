import numpy as np

error_file = open("errors_all.txt", "r")


def distance(a, b):
    # Calculates the Levenshtein distance between a and b

    n, m = len(a), len(b)
    inverse = False
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
        inverse = True

    max_distance = m + n  # to avoid index out of range in possible_action creation, fictive column
    current_row = list(range(n + 1)) + [max_distance]  # Keep current and previous row, not entire matrix

    matrix = np.array([current_row])
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n + [max_distance]
        for j in range(1, n + 1):
            # add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            add, delete, change = previous_row[j] + 1, \
                                  current_row[j - 1] + 1, \
                                  previous_row[j - 1] + int(a[j - 1] != b[i - 1])
            # if a[j - 1] != b[i - 1]:
            #     change += 1
            current_row[j] = min(add, delete, change)

        matrix = np.vstack((matrix, [current_row]))

    lev_distance = current_row[n]
    # print(matrix)

    if inverse:
        matrix = matrix.T
        a, b = b, a
        n, m = m, n

    position = [n, m, lev_distance]  # [x,y, distance]
    while position[2] != 0:  # пока position не придет в правый нижний угол
        x, y = position[0], position[1]

        possible_actions = [matrix[y - 1][x - 1],  # change
                            matrix[y - 1][x],  # add
                            matrix[y][x - 1]]  # delete
        action = np.argmin(possible_actions)

        if action == 0:  # change
            if position[2] != possible_actions[action.item()]:
                position[2] -= 1
                print(a[x - 1] + " -> " + b[y - 1])
                # print(2)
            position[0] -= 1
            position[1] -= 1
        elif action == 1:  # add if not inverse
            if position[2] != possible_actions[action.item()]:
                position[2] -= 1
                print("_ -> " + b[y - 1])
                # print(0)
            position[1] -= 1
        else:  # delete if not inverse
            if position[2] != possible_actions[action.item()]:
                position[2] -= 1
                print(a[x - 1] + " ->_")
                # print(1)
            position[0] -= 1

    return lev_distance


# for line in error_file:
#     delimiter = line.find("	")
#     query = (line[: delimiter - 1].split(" "), line[delimiter + 1:].split(" "))

a1 = "mmp"
b1 = "govno"
print(distance(a1, b1))  # a to b
print(distance(b1, a1))  # b to a
