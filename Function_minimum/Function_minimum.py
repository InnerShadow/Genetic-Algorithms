import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Get_Elitizme import eaSimpleElitizme

LOW = -5
UP = 5
ETTA = 20
LENGHT_CHROM = 2

POPULATION_SIZE = 200
P_CROSSOVER = 0.9
P_MUTATION = 0.2
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 5

def randomSpot(a, b):
	return [random.uniform(a, b), random.uniform(a, b)]


def himmelblalu(individual): #fitness
	x, y = individual
	f = (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
	return f,


def show(ax, xgrid, ygrid, f, population):

	time.sleep(0.5)

	ptMins = [[3.0, 2.0], [-2.805118, 3.131312], [-3.779310, -3.283186], [3.584458, -1.848126]]

	ax.clear()
	ax.contour(xgrid, ygrid, f)
	ax.scatter(*zip(*ptMins), marker = 'X', color = 'red', zorder = 1)
	ax.scatter(*zip(*population), color = 'green', s = 2, zorder = 0)

	plt.draw()
	plt.gcf().canvas.flush_events()


def __main__():
	hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

	creator.create("FitnessMin", base.Fitness, weights = (-1.0, ))
	creator.create("Individual", list, fitness = creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register("randomSpot", randomSpot, LOW, UP)
	toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomSpot)
	toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

	toolbox.register("evaluate", himmelblalu)
	toolbox.register("select", tools.selTournament, tournsize = 3)
	toolbox.register("mate", tools.cxSimulatedBinaryBounded, low = LOW, up = UP, eta = ETTA)
	toolbox.register("mutate", tools.mutPolynomialBounded, low = LOW, up = UP, eta = ETTA, indpb = 1.0 / LENGHT_CHROM)

	stats = tools.Statistics(lambda ind : ind.fitness.values)
	stats.register("min", np.min)
	stats.register("avg", np.mean)

	x = np.arange(-5, 5, 0.1)
	y = np.arange(-5, 5, 0.1)
	xgrid, ygrid = np.meshgrid(x, y)

	f_himmelbalu = (xgrid ** 2 + ygrid - 11) ** 2 + (xgrid + ygrid ** 2 - 7) ** 2

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(5, 5)

	ax.set_xlim(LOW - 3, UP + 3)
	ax.set_ylim(LOW - 3, UP + 3)

	population = toolbox.populationCreator(n = POPULATION_SIZE)

	population, logbook = eaSimpleElitizme(population, toolbox, cxpb = P_CROSSOVER, mutpb = P_MUTATION, ngen = MAX_GENERATIONS, 
		halloffame = hof, stats = stats, callback = (show, (ax, xgrid, ygrid, f_himmelbalu, population)), verbose = True)

	maxFitnessValues, meanFitnessValues = logbook.select("min", "avg")

	best = hof.items[0]
	print(best)

	plt.ioff()
	plt.show()

	plt.plot(maxFitnessValues, color = 'red')
	plt.plot(meanFitnessValues, color = 'green')
	plt.xlabel('Generation')
	plt.ylabel('Max/Avg fitness')
	plt.show()


if __name__ == '__main__':
	__main__()
