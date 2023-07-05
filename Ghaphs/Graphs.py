import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Graphs_show import show_graph

POPULATION_SIZE = 1000
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 1

inf = 100

Matrix = 	((0,	 3, 	1, 	3, 	inf, 	inf),
		(3,	 0, 	4, 	inf, 	inf, 	inf),
		(1,	 4, 	0, 	inf, 	7, 	4),
		(3,	 inf, 	inf,	0, 	inf, 	2),
		(inf,	 inf, 	7, 	inf, 	0, 	4),
		(inf,	 inf, 	4, 	2, 	4, 	0))

start = 5

LENGHT_MATRIX = len(Matrix)
LENGHT_CHROM = len(Matrix) * len(Matrix[0])


def GetFitness(individual):
	s = 0
	for n, path in enumerate(individual):
		path = path[:path.index(n) + 1]

		i = start
		for j in path:
			s += Matrix[i][j]
			i = j

	return s,


def cxOrdered(ind1, ind2):
	for p1, p2 in zip(ind1, ind2):
		tools.cxOrdered(p1, p2)

	return ind1, ind2


def mutShuffleIndexes(individual, indpb):
	for ind in individual:
		tools.mutShuffleIndexes(ind, indpb)

	return individual, 


def __main__():

	hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

	creator.create("FitnessMin", base.Fitness, weights = (-1.0, ))
	creator.create("Individual", list, fitness = creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register("randomOrder", random.sample, range(LENGHT_MATRIX), LENGHT_MATRIX)
	toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.randomOrder, LENGHT_MATRIX)
	toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

	toolbox.register("evaluate", GetFitness)
	toolbox.register("select", tools.selTournament, tournsize = 3)
	toolbox.register("mate", cxOrdered)
	toolbox.register("mutate", mutShuffleIndexes, indpb = 1.0 / LENGHT_CHROM / 10)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("min", np.min)
	stats.register("avg", np.mean)

	population = toolbox.populationCreator(n = POPULATION_SIZE)

	population, logbook = algorithms.eaSimple(population, toolbox, cxpb = P_CROSSOVER / LENGHT_MATRIX,
		mutpb = P_MUTATION / LENGHT_MATRIX, ngen = MAX_GENERATIONS, stats = stats, halloffame = hof,
		verbose = True)

	maxFitnessValues, meanFutnessValues = logbook.select("min", "avg")

	best = hof.items[0]
	print("\n", best, "\n")

	plt.plot(maxFitnessValues, color = 'red')
	plt.plot(meanFutnessValues, color = 'green')
	plt.xlabel('Generations')
	plt.ylabel('Max/avg fitness')

	plt.show()

	fig, ax = plt.subplots()
	show_graph(ax, best, start, Matrix, inf)
	plt.show()


if(__name__ == '__main__'):
    __main__()
