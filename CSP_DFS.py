# This is a Control Satisfaction Problem using depth-first searches
# David Bush, Project 3, CS 470 Soule, 06/04/2021

import copy
import time


start = time.time()
num = 5
num_vars = 30
num_colors = 4  # 0, 1, 2, 3

neighbor_test = [[2, 5], [1, 3, 4, 5], [2, 4, 5], [2, 3], [1, 2, 3]] # x1, x2, x3, x4, x5

neighbor_list = [[2, 3, 15, 29], [1, 21, 22], [1, 7, 10, 18, 19, 24, 28], [22, 29, 30],     # x1, x2, x3, x4
                 [14, 15, 27, 29], [12, 20, 22, 28], [3, 8, 27], [10, 11, 17, 19],    # x5, x6, x7, x8
                 [10, 11, 23, 29], [3, 8, 9, 11, 24], [8, 9, 10, 14, 17, 18, 23],   # x9, x10, x11
                 [6, 13, 14, 24], [12, 15, 26], [5, 11, 12, 18, 24, 29, 30],   # x12, x13, x14
                 [1, 5, 13, 22, 23, 27], [25], [8, 11, 29, 30], [8, 11, 21, 25, 29],    # x15, x16, x17, x18
                 [3, 8, 30], [6], [2, 18, 23, 26], [2, 4, 6, 15, 24, 25, 27, 30],  # x19, x20, x21, x22
                 [9, 11, 15, 21, 28], [3, 10, 12, 14, 22], [16, 18, 22, 29], [13, 21],    # x23, x24, x25, x26
                 [5, 7, 15, 22], [3, 6, 23], [1, 4, 5, 9, 14, 17, 18, 25, 30],  # x27, x28, x29
                 [4, 14, 17, 19, 22, 29]]   # x30
variable_list = []
domain_list = []
solution = []


class Variable:
    def __init__(self, name, neighbors):
        self.name = name            # x1-x30
        self.neighbors = neighbors  # List of neighboring variables

    def __lt__(self, other):
        if len(self.neighbors) < len(other.neighbors) :
            return False
        return True


def print_list(var_list):
    for var in var_list:
        print("x", var.name, " neighbors: ", var.neighbors)


def count_conflicts(var_list, sol_list):
    conflicts = 0
    for var in var_list:
        for neigh in var.neighbors:
            if sol_list[var.name-1] == sol_list[neigh-1] and sol_list[var.name-1] != -1 and sol_list[neigh-1] != -1:
                conflicts += 1
    return conflicts


def fully_assigned(s):
    for k in range(0, len(s)):
        if s[k] == -1:
            return False
    return True


def remove_domains(dom, neighbors, c):
    for val in neighbors:
        if not domain_zero(dom, val-1) and c in dom[val-1]:
            dom[val-1].remove(c)


def domain_zero(dom, var):
    if len(dom[var]) == 0:
        return True
    return False


def search_solution(s, var):
    for c in range(0, num_colors):
        s2 = copy.deepcopy(s)
        s2[var] = c
        print(var+1, s2,  count_conflicts(variable_list, s2))
        if count_conflicts(variable_list, s2) == 0:  # no conflicts
            if fully_assigned(s2):
                # print(var + 1, s2, count_conflicts(variable_list, s2))
                return True
            else:
                search_solution.x = search_solution.x + 1
                tmp = search_solution(s2, var+1)
                if tmp:
                    return True
    return False    # no solution


def ss_ordering(s, var):
    for color in range(0, num_colors):
        s2 = copy.deepcopy(s)
        s2[variable_list[var].name-1] = color
        print(variable_list[var].name, s2,  count_conflicts(variable_list, s2))
        if count_conflicts(variable_list, s2) == 0:  # no conflicts
            if fully_assigned(s2):  # found solution
                return True
            else:   # search for next variable
                tmp = ss_ordering(s2, var+1)
                if tmp:
                    return True
    return False    # no solution


def ss_forward_check(s, var, dom):
    for color in dom[variable_list[var].name-1]:
        s2 = copy.deepcopy(s)
        s2[variable_list[var].name-1] = color
        dom2 = copy.deepcopy(dom)
        dom2[variable_list[var].name-1].remove(color)
        print(variable_list[var].name, s2,  count_conflicts(variable_list, s2), dom2)
        remove_domains(dom2, variable_list[var].neighbors, color)
        if count_conflicts(variable_list, s2) == 0:  # no conflicts
            if fully_assigned(s2):  # found solution
                print(variable_list[var].name, s2, count_conflicts(variable_list, s2), dom2)
                return True
            else:   # search for next variable
                if domain_zero(dom2, variable_list[var+1].name-1):
                    return False
                tmp = ss_forward_check(s2, var+1, dom2)
                if tmp:
                    return True
    return False    # no solution


# initialize variable list
for z in range(1, num_vars+1, 1):
    v = Variable(z, neighbor_list[z-1])
    variable_list.append(v)
# initialize domain list
for n in range(0, num_vars):
    color_list = []
    for cx in range(0, num_colors):
        color_list.append(cx)
    domain_list.append(color_list)
# initialize solution
for i in range(num_vars):
    solution.append(-1)

# print_list(variable_list)
search_solution.x = 0
search_solution(solution, 0)   # basic depth first search

# variable_list.sort()    # sort list by num of neighbors
# print_list(variable_list)
# ss_ordering(solution, 0)    # depth first search with heuristic

# ss_forward_check(solution, 0, domain_list)    # forward check + heuristic

print("Number of recursive calls: ", search_solution.x)
end = time.time()
print("time: ", end-start)
