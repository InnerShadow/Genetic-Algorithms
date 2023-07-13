import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Show_path import show_path	
from Get_Field import Get_clear_field, Get_one_onbtacle_field, Get_random_field, GetMazeField

#random.seed(69)

class FitnessMax():
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()	


FIELD_SIZE = 50

len_steps = [0.1, 0.2, 0.3, 0.4]
generations_steps = [0.1, 0.2, 0.4, 0.6]

LENGHT_CHROM = int(2.5 * FIELD_SIZE)
POPULATION_SIZE = 100 * FIELD_SIZE
P_CROSSOVER = 0.9
P_MUTATION = 0.2
MAX_GENERATIONS = 3 * FIELD_SIZE + 25
HALL_OF_FAME_SIZE = int(0.05 * LENGHT_CHROM)

start = (5, 20) #(random.randint(1, FIELD_SIZE - 2), random.randint(1, FIELD_SIZE - 2))
finish = (45, 20) #(random.randint(1, FIELD_SIZE - 2), random.randint(1, FIELD_SIZE - 2))

inf = int(0.4 * FIELD_SIZE)
hall_of_fame_inf = -10000 * FIELD_SIZE

# field:
	# 0 - avaliable cell
	# 1 - barrier

field = GetMazeField(FIELD_SIZE, start, finish)

#path:
	# 0 - stay
	# 1 - up
	# 2 - down
	# 3 - right
	# 4 - left

def randomPath():
	path = []
	for n in range(int(LENGHT_CHROM * len_steps[0])):
		path.extend([random.randint(1, 4)])

	return Individual(path)


def AdditionrandomPath(lenght):
	path = []
	for n in range(lenght):
		path.extend([random.randint(1, 4)])

	return Individual(path)


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

	if it == len(individual):
		fitness += np.sqrt(abs(currntX - finish[1]) ** 2 + abs(currntY - finish[0]) ** 2)

	fitness *= -1

	return fitness,


def ZeroPathFitness(individual):
	currntX = start[1]
	currntY = start[0]

	fitness = 0
	it = 0

	for i in range(len(individual)):
		if individual[i] == 1:
			currntY += 1
			if currntY > FIELD_SIZE - 1 or field[currntX][currntY] == 1:
				currntY -= 1
				individual[i] = 0
				#fitness += inf

		if individual[i] == 2:
			currntY -= 1
			if currntY < 0 or field[currntX][currntY] == 1:
				currntY += 1
				individual[i] = 0
				#fitness += inf

		if individual[i] == 3:
			currntX += 1
			if currntX > FIELD_SIZE - 1 or field[currntX][currntY] == 1:
				currntX -= 1
				individual[i] = 0
				#fitness += inf

		if individual[i] == 4:
			currntX -= 1
			if currntX < 0 or field[currntX][currntY] == 1:
				currntX += 1
				individual[i] = 0
				#fitness += inf

		fitness += 1

		if currntX == finish[1] and currntY == finish[0]:
			break
		it += 1

	if it == len(individual):
		fitness += np.sqrt(abs(currntX - finish[1]) ** 2 + abs(currntY - finish[0]) ** 2)

	fitness *= -1

	return fitness, 


def clone(value):
    ind = Individual(value[:])
    ind.fitness.values[0] = value.fitness.values[0]
    return ind


def populationCreator(n = 0):
    return list([randomPath() for i in range(n)])


def selTournament(population, p_len):
    offspring = []
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, p_len - 1), random.randint(0, p_len - 1), random.randint(0, p_len - 1)

        offspring.append(max([population[i1], population[i2], population[i3]], key = lambda ind: ind.fitness.values[0]))

    return offspring


def cxOnePoint(child1, child2):
    s = random.randint(2, len(child1) - 3)
    child1[s:], child2[s:] = child2[s:], child1[s:]


def cxTwoPoint(child1, child2):
	s1 = random.randint(2, len(child1) - 3)
	s2 = random.randint(2, len(child1) - 3)
	if s1 > s2:
		s1, s2 = s2, s1

	child1[s1:s2], child2[s1:s2] = child2[s1:s2], child1[s1:s2]


def MutPath(individual, indpb):
	for i in range(len(individual)):
		if random.random() < indpb:
			individual[i] = random.randint(1, 4)

	return individual,


def Get_Hall_of_Fame(population, fitnessValues):

	valus = fitnessValues.copy()

	hof = [LENGHT_CHROM] * HALL_OF_FAME_SIZE

	for i in range(HALL_OF_FAME_SIZE):
		best_index = valus.index(max(valus))
		hof[i] = population[best_index]
		valus[best_index] = hall_of_fame_inf

	return hof


def show(ax, hof):
	#time.sleep(0.5)
	ax.clear()
	#show_path(ax, hof.items[2], field, start, finish, 'blue')
	show_path(ax, hof[len(hof) - 1], field, start, finish, 'green')
	show_path(ax, hof[0], field, start, finish, 'red')

	plt.draw()
	plt.gcf().canvas.flush_events() 


def __main__():

	hof = [0] * HALL_OF_FAME_SIZE

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(FIELD_SIZE, FIELD_SIZE)

	ax.set_xlim(-2, FIELD_SIZE + 3)
	ax.set_ylim(-2, FIELD_SIZE + 3)

	population = populationCreator(n = POPULATION_SIZE + HALL_OF_FAME_SIZE)
	generationCounter = 0

	fitnessValues = list(map(ZeroPathFitness, population))

	for individual, fitnessValue in zip(population, fitnessValues):
		individual.fitness.values = fitnessValue

	maxFitnessValues = []
	meanFitnessValues = []

	normedMaxFitnessValues = []
	normedMeanFitnessValues = []

	fitnessValues = [individual.fitness.values[0] for individual in population]

	while generationCounter < MAX_GENERATIONS:
		generationCounter += 1

		for i in range(1, len(len_steps)):
			if generationCounter == int(generations_steps[i] * MAX_GENERATIONS):
				for j in range(len(population)):
					path = AdditionrandomPath(int(LENGHT_CHROM * len_steps[i]))
					population[j].extend(path)

		offspring = selTournament(population, len(population))
		offspring = list(map(clone, offspring))

		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < P_CROSSOVER:
				cxTwoPoint(child1, child2)

		for mutant in offspring:
			if random.random() < P_MUTATION:
				MutPath(mutant, indpb = 10.0 / len(population[0]))

		freshFitnessValues = list(map(ZeroPathFitness, offspring))
		for individual, fitnessValue in zip(offspring, freshFitnessValues):
			individual.fitness.values = fitnessValue

		population[:] = offspring

		fitnessValues = [ind.fitness.values[0] for ind in population]

		hof = Get_Hall_of_Fame(population, fitnessValues)

		for i in range(HALL_OF_FAME_SIZE):
			population[POPULATION_SIZE + i] = hof[i]

		maxFitness = max(fitnessValues) * -1
		meanFitness = sum(fitnessValues) / len(population) * -1
		maxFitnessValues.append(maxFitness)
		meanFitnessValues.append(meanFitness)

		normedMaxFitnessValues.append(maxFitness / len(population[0]))
		normedMeanFitnessValues.append(meanFitness / len(population[0]))

		print(f"Generation {generationCounter}: Max = {maxFitness}, Avg = {meanFitness}")

		show(ax, hof)

	plt.ioff()
	plt.show()

	plt.plot(maxFitnessValues, color = 'red')
	plt.plot(meanFitnessValues, color = 'green')
	plt.xlabel("Generation")
	plt.ylabel("Max/avg fitness")
	plt.show()

	plt.plot(normedMaxFitnessValues, color = 'red')
	plt.plot(normedMeanFitnessValues, color = 'green')
	plt.xlabel("Generation")
	plt.ylabel("Normed Max/avg fitness")
	plt.show()


if __name__ == '__main__':
	__main__()

