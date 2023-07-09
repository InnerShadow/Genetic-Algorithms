import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Get_Elitizme import eaSimpleElitizme
from Show_path import show_path	
from Get_Field import Get_clear_field, Get_one_onbtacle_field, Get_random_field

FIELD_SIZE = 50

LENGHT_CHROM = int(2 * FIELD_SIZE)
POPULATION_SIZE = 100 * FIELD_SIZE
P_CROSSOVER = 0.9
P_MUTATION = 0.5
MAX_GENERATIONS = 3 * FIELD_SIZE + 25
HALL_OF_FAME_SIZE = int(0.05 * LENGHT_CHROM)

start = (random.randint(1, FIELD_SIZE - 2), random.randint(1, FIELD_SIZE - 2))
finish = (random.randint(1, FIELD_SIZE - 2), random.randint(1, FIELD_SIZE - 2))

inf = int(0.2 * FIELD_SIZE)

# field:
	# 0 - avaliable cell
	# 1 - barrier

field = Get_random_field(FIELD_SIZE, start, finish)

#path:
	# 0 - stay
	# 1 - up
	# 2 - down
	# 3 - right
	# 4 - left

def randomPath():
	path = []
	for n in range(LENGHT_CHROM):
		path.extend([random.randint(1, 4)])

	return creator.Individual(path)


def MutPath(individual, indpb):
	for i in range(len(individual)):
		if random.random() < indpb:
			individual[i] = random.randint(1, 4)

	return individual,


def show(ax, hof):
	#time.sleep(0.5)
	ax.clear()
	#show_path(ax, hof.items[2], field, start, finish, 'blue')
	show_path(ax, hof.items[len(hof) - 1], field, start, finish, 'green')
	show_path(ax, hof.items[0], field, start, finish, 'red')

	plt.draw()
	plt.gcf().canvas.flush_events()


def pathFitness(individual):
	currntX = start[1]
	currntY = start[0]

	fitness = 0
	it = 0

	for i in range(len(individual)):
		if individual[i] == 1:
			currntY += 1
			if currntY > FIELD_SIZE - 1:
				currntY -= 1
				individual[i] = 0
				fitness += inf

		if individual[i] == 2:
			currntY -= 1
			if currntY < 0:
				currntY += 1
				individual[i] = 0
				fitness += inf

		if individual[i] == 3:
			currntX += 1
			if currntX > FIELD_SIZE - 1:
				currntX -= 1
				individual[i] = 0
				fitness += inf

		if individual[i] == 4:
			currntX -= 1
			if currntX < 0:
				currntX += 1
				individual[i] = 0
				fitness += inf

		if field[currntX][currntY] == 0:
			fitness += 1
		else:
			fitness += inf

		if currntX == finish[1] and currntY == finish[0]:
			break
		it += 1

	if it == LENGHT_CHROM:
		fitness += np.sqrt(abs(currntX - finish[1]) ** 2 + abs(currntY - finish[0]) ** 2)

	return fitness, 


def __main__():

	hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

	creator.create("FitnessMin", base.Fitness, weights = (-1.0, ))
	creator.create("Individual", list, fitness = creator.FitnessMin)

	toolbox = base.Toolbox()
	toolbox.register("randomPath", randomPath)
	toolbox.register("populationCreator", tools.initRepeat, list, toolbox.randomPath)

	toolbox.register("evaluate", pathFitness)
	toolbox.register("select", tools.selTournament, tournsize = 3)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", tools.mutShuffleIndexes, indpb = 1.0 / LENGHT_CHROM)

	stats = tools.Statistics(lambda ind : ind.fitness.values)
	stats.register("min", np.min)
	stats.register("avg", np.mean)

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(FIELD_SIZE, FIELD_SIZE)

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


if __name__ == '__main__':
	__main__()
