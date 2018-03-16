#!/usr/bin/env python3

import math
import numpy
import sys
import random
from optparse import OptionParser

type_of_function = 0


def fun(member):
    if type_of_function == 1:
        return math.sin(member[0]) * math.cos(member[1])
    elif type_of_function == 2:
        return math.sin(member[0]) * math.cos(member[1]) + member[0] + member[1]
    else:
        return math.sin(member[0]) * math.sin(member[1]) + member[0]**2 + member[1]**2


# Przylklady wywolania:
#  $ python3 main.py -t 1 < population2.txt
#  $ python3 main.py -t 2 < population2.txt
#  $ python3 main.py -t 3 < population2.txt
#  $ python3 main.py -t 1 < population.txt
#  $ python3 main.py -t 2 < population.txt
#  $ python3 main.py -t 3 < population.txt


def main():
    parser = OptionParser()
    parser.add_option('-t', type="int", dest="fun_type")
    (arguments, args) = parser.parse_args()

    if arguments.fun_type > 0:
        try:
            type_of_function = int(arguments.fun_type)
        except:
            type_of_function = 1

        population0 = []
        population1 = []
        for line in sys.stdin.readlines():
            population0.append([float(n) for n in line.split()])
            population1.append([float(n) for n in line.split()])

        print("#  ---------------- 0. strategia (mi + 1) -------------- #")
        mi = len(population0) - 1
        for iteration in range(mi):
            fitness = population_fitness(population0)
            the_most_weak_member = fitness.index(max(fitness))
            #  ------------ mutacja (w tej strategii nie ma krzyzowania) ------ #
            population0[the_most_weak_member] = gaussian_mutation(population0[the_most_weak_member])
            # lub
            # population0[the_most_weak_member] = gaussian_mutation(population0[the_most_weak_member])

            fitness = population_fitness(population0)
            population0.remove(population0[fitness.index(max(fitness))])
        print("Przetrwał osobnik postaci: " + str(" ".join(map(str, population0[0]))))

        print("#  ---------------- 1. SGA, selekcja turniejowa -------------- #")
        mi = len(population1) - 1
        for iteration in range(mi):
            #  --- selekcja sposrod  m = 2  osobnikow
            m1_idx = random.randint(0, len(population1) - 1)
            m2_idx = random.randint(0, len(population1) - 1)

            if fitness_fun(population1[m1_idx], population1) < fitness_fun(population1[m2_idx], population1):
                population1.remove(population1[m2_idx])
            else:
                population1.remove(population1[m1_idx])
        print("Przetrwał osobnik postaci: " + str(" ".join(map(str, population1[0]))))


def fitness_fun(member, population):
    minimum = min([fun(i) for i in population])
    maximum = max([fun(i) for i in population])
    try:
        return abs(minimum * fun(member) / maximum)
    except ZeroDivisionError:
        return abs(minimum + fun(member))


def population_fitness(population):
    evaluations = []
    for item in population:
        evaluations.append(fitness_fun(item, population))
    return evaluations


# ------------ ways to mutate -----------#
def gaussian_mutation(member):
    return [(i - numpy.random.normal(0.0, 1.0, None)) for i in member]


def uniform_mutation(member):
    return [(i - random.uniform()) for i in member]


# ------------ ways to crossing -----------#
def abs_crossing(member1, member2):
    # return [(member1[i] * member2[i]) / 2 for i in range(0, len(member1))]
    return 0


def other_crossing(member1, member2):
    # return [(member1[i] * member2[i]) / 2 for i in range(0, len(member1))]
    return 0


if __name__ == '__main__':
    main()
