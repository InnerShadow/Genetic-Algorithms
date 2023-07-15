import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Show_path import show_path, show_greed	
from Get_Field import Get_clear_field, Get_one_onbtacle_field, Get_random_field, GetMazeField

colors = ['black', 'brown', 'purple', 'pink', 'cyan', 'blue', 'green', 'yellow', 'orange', 'red']

#random.seed(8014)

#	     fitness x  y ngen
cutData = [0   , 0, 0, 0]

class FitnessMax():
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()	


FIELD_SIZE = 50

startChromo = FIELD_SIZE

MAX_GENERATIONS = 3 * FIELD_SIZE + 25
LENGHT_CHROM = int(2.5 * FIELD_SIZE)
POPULATION_SIZE = 100 * FIELD_SIZE
P_CROSSOVER = 0.9
P_MUTATION = 0.3
HALL_OF_FAME_SIZE = int(0.08 * LENGHT_CHROM)

find_finish = False

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
	for n in range(int(startChromo)):
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


def MazePathFitness(individual):

	global find_finish

	currntX = start[1]
	currntY = start[0]

	currentField = field.copy()

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

		currentField[currntX][currntY] = 2

		fitness += 1

		if currntX == finish[1] and currntY == finish[0]:
			fitness -= (FIELD_SIZE)
			find_finish = True
			break
		it += 1

	if it == len(individual):
		fitness += np.sqrt(abs(currntX - finish[1]) ** 2 + abs(currntY - finish[0]) ** 2)

	benefits = np.count_nonzero(currentField == 2)

	fitness -= int(benefits * 2.5)

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

	hof = [0] * HALL_OF_FAME_SIZE

	for i in range(HALL_OF_FAME_SIZE):
		best_index = valus.index(max(valus))
		hof[i] = population[best_index]
		valus[best_index] = hall_of_fame_inf

	return hof


def GetCurrentXY(individual):
	currntX = start[1]
	currntY = start[0]

	it = 0

	for i in range(len(individual)):
		if individual[i] == 1:
			currntY += 1
			if currntY > FIELD_SIZE - 1 or field[currntX][currntY] == 1:
				currntY -= 1
				individual[i] = 0

		if individual[i] == 2:
			currntY -= 1
			if currntY < 0 or field[currntX][currntY] == 1:
				currntY += 1
				individual[i] = 0

		if individual[i] == 3:
			currntX += 1
			if currntX > FIELD_SIZE - 1 or field[currntX][currntY] == 1:
				currntX -= 1
				individual[i] = 0

		if individual[i] == 4:
			currntX -= 1
			if currntX < 0 or field[currntX][currntY] == 1:
				currntX += 1
				individual[i] = 0

		if currntX == finish[1] and currntY == finish[0]:
			break
		it += 1

	return currntX, currntY,


def cutHalf(individual):
	individual[:] = individual[:int(len(individual) * 0.25)]
	return individual


def show(ax, hof):
	#time.sleep(0.5)
	ax.clear()
	show_greed(ax, field, start, finish)

	hofScail = len(hof) / len(colors)

	lineScale = 10 / len(colors)

	for i in range(len(colors)):
		show_path(ax, hof[int(len(hof) - i * hofScail) - 1], field, start, finish, colors[i], 1.5 + (len(colors) - i) * lineScale)

	plt.draw()
	plt.gcf().canvas.flush_events() 


def __main__():

	global find_finish

	global MAX_GENERATIONS

	hof = [0] * HALL_OF_FAME_SIZE

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(FIELD_SIZE, FIELD_SIZE)

	ax.set_xlim(-2, FIELD_SIZE + 3)
	ax.set_ylim(-2, FIELD_SIZE + 3)

	population = populationCreator(n = POPULATION_SIZE + HALL_OF_FAME_SIZE)
	generationCounter = 0

	fitnessValues = list(map(MazePathFitness, population))

	for individual, fitnessValue in zip(population, fitnessValues):
		individual.fitness.values = fitnessValue

	maxFitnessValues = []
	meanFitnessValues = []

	normedMaxFitnessValues = []
	normedMeanFitnessValues = []

	fitnessValues = [individual.fitness.values[0] for individual in population]

	while generationCounter < MAX_GENERATIONS:
		generationCounter += 1

		if cutData[3] == 8:
			MAX_GENERATIONS += int(FIELD_SIZE * 1.5)
			for i in range(len(population)):
				population[i] = cutHalf(population[i])

		for j in range(len(population)):
			path = AdditionrandomPath(int(0.05 * LENGHT_CHROM))
			population[j].extend(path)

		offspring = selTournament(population, len(population))
		offspring = list(map(clone, offspring))

		offspring = offspring[:-HALL_OF_FAME_SIZE]

		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < P_CROSSOVER:
				cxTwoPoint(child1, child2)

		for mutant in offspring:
			if random.random() < P_MUTATION:
				MutPath(mutant, indpb = 10.0 / len(population[0]))

		freshFitnessValues = list(map(MazePathFitness, offspring))
		for individual, fitnessValue in zip(offspring, freshFitnessValues):
			individual.fitness.values = fitnessValue

		fitnessValues = [ind.fitness.values[0] for ind in offspring]

		if generationCounter != 1:
			currntX, currntY = GetCurrentXY(hof[0])
			cutData[1] = currntX
			cutData[2] = currntY

		hof = Get_Hall_of_Fame(offspring, fitnessValues)

		offspring.extend(hof)

		population[:] = offspring

		currntX, currntY = GetCurrentXY(hof[0])
		if (abs(currntX - cutData[1]) + abs(currntY - cutData[2])) <= 3 and not find_finish:  
			cutData[3] += 1
		else:
			cutData[3] = 0

		maxFitness = max(fitnessValues) * -1
		meanFitness = sum(fitnessValues) / len(population) * -1
		maxFitnessValues.append(maxFitness)
		meanFitnessValues.append(meanFitness)

		normedMaxFitnessValues.append(maxFitness / len(population[0]))
		normedMeanFitnessValues.append(meanFitness / len(population[0]))

		print(f"Generation {generationCounter}: Max = {maxFitness}, Avg = {meanFitness}")

		show(ax, hof)

		#print(cutData, find_finish)

	print(hof[0])

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

