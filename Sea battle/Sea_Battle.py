import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Get_Elitizme import eaSimpleElitizme
from Show_ships import show_ships

FIELD_SIZE = 10
SHIPS = 10
LENGHT_CHROM = 3 * SHIPS

POPULATION_SIZE = 50
P_CROSSOVER = 0.9
P_MUTATION = 0.2
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 1

inf = 1000

def show(ax, hof):
	time.sleep(1)
	ax.clear()
	show_ships(ax, hof.items[0], FIELD_SIZE)

	plt.draw()
	plt.gcf().canvas.flush_events()


def randomShip(total):
	ships = []
	for n in range(total):
		ships.extend([random.randint(1, FIELD_SIZE), random.randint(1, FIELD_SIZE), random.randint(0, 1)])

	return creator.Individual(ships)


def shipsFitness(individual):
	type_ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

	P0 = np.zeros((FIELD_SIZE, FIELD_SIZE))
	P = np.ones((FIELD_SIZE + 6, FIELD_SIZE + 6)) * inf
	P[1:FIELD_SIZE + 1, 1:FIELD_SIZE + 1] = P0

	th = 0.2
	h = np.ones((3, 6)) * th
	ship_one = np.ones((1, 4))
	v = np.ones((6, 3)) * th

	for *ship, t in zip(*[iter(individual)] * 3, type_ship):
		if ship[-1] == 0:
			sh = np.copy(h[:, :t + 2])
			sh[1, 1:t + 1] = ship_one[0, :t]
			P[ship[0] - 1:ship[0] + 2, ship[1] - 1:ship[1] + t + 1] += sh
		else:
			sh = np.copy(v[:t + 2, :])
			sh[1:t + 1, 1] = ship_one[0, :t]
			P[ship[0] - 1:ship[0] + t + 1, ship[1] - 1:ship[1] + 2] += sh


	s = np.sum(P[np.bitwise_and(P > 1, P < inf)])
	s += np.sum(P[P > inf + th * 4])

	return s,


def MutShip(individual, indpb):
	for i in range(len(individual)):
		if random.random() < indpb:
			individual[i] = random.randint(0, 1) if (i + 1) % 3 == 0 else random.randint(1, FIELD_SIZE)

	return individual,


def __main__():
	hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

	creator.create("FitnessMin", base.Fitness, weights = (-1.0, ))
	creator.create("Individual", list, fitness = creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register("randomShip", randomShip, SHIPS)
	toolbox.register("populationCreator", tools.initRepeat, list, toolbox.randomShip)

	toolbox.register("evaluate", shipsFitness)
	toolbox.register("select", tools.selTournament, tournsize = 3)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", MutShip, indpb = 1.0 / LENGHT_CHROM)

	stats = tools.Statistics(lambda ind : ind.fitness.values)
	stats.register("min", np.min)
	stats.register("avg", np.mean)

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(6, 6)

	ax.set_xlim(-2, FIELD_SIZE + 3)
	ax.set_ylim(-2, FIELD_SIZE + 3)

	population = toolbox.populationCreator(n = POPULATION_SIZE)

	population, logbook = eaSimpleElitizme(population, toolbox, cxpb = P_CROSSOVER, mutpb = P_MUTATION, ngen = MAX_GENERATIONS,
		halloffame = hof, stats = stats, callback = (show, (ax, hof, )), verbose = True)

	plt.ioff()
	plt.show()

	maxFitnessValues, meanFitnessValues = logbook.select("min", "avg")

	best = hof.items[0]
	print(best)

	plt.plot(maxFitnessValues, color = 'red')
	plt.plot(meanFitnessValues, color = 'green')
	plt.xlabel("Generation")
	plt.ylabel("Max/avg fitness")
	plt.show()

	# fig, ax = plt.subplots()
	# fig.set_size_inches(6, 6)

	# show_ships(ax, best, FIELD_SIZE)
	# plt.show()



if __name__ == '__main__':
	__main__()

