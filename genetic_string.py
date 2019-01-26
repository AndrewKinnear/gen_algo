#Going to look in to some optimizations for gen algos. Including a different way for crossover and determening fitness
#Oh lord lets try again


import random

# Class to hold list of individuals
class Population:

    individual_list = []

    def __init__(self, my_list=None):
        self.individual_list = my_list

    def get_individual(self, index):
        return self.individual_list[index]

# Class to hold the individuals
class Individual:

    def __init__(self, genes=None, fitness=None, age=None):
        self.genes = genes
        self.fitness = fitness
        self.age = age

    def get_fitness(self):
        return self.fitness

# Returns fittest indv from given population
def get_fittest(population):
    fittest = -1
    fittest_index = -1
    i = 0

    while i < len(population.individual_list):
        temp_fitness = population.individual_list[i].fitness
        if temp_fitness > fittest:
            fittest = temp_fitness
            fittest_index = i
        i += 1
    return population.individual_list[fittest_index]


# Returns fittest indv from given population
def get_ham_fittest(population):
    fittest = 9999999 #TODO Bring in length of string + 1
    fittest_index = -1
    i = 0 

    while i < len(population.individual_list):
        temp_fitness = population.individual_list[i].fitness
        if temp_fitness < fittest:
            fittest = temp_fitness
            fittest_index = i
        i += 1

    return population.individual_list[fittest_index]



# Returns the given amount of the fittest population
def get_ham_fittest_el(population, amount):
    j = 0
    temp_list = []

    while j < amount:
        fittest = 9999999 #TODO Bring in length of string + 1
        fittest_index = -1
        i = 0
        while i < len(population.individual_list):
            temp_fitness = population.individual_list[i].fitness
            if temp_fitness < fittest:
                fittest = temp_fitness
                fittest_index = i
            i += 1
        j += 1
        population.individual_list.remove(population.individual_list[fittest_index])
        temp_list.append(population.individual_list[fittest_index])
    
    return temp_list

# Creates new population by target size, also sets indv fitness determined by the target
def create_population(pop_size, target):
    my_list = []
    for i in range(pop_size):
        my_list.append(Individual(create_genes(len(target)), 0, 0))
    population = Population(my_list)
    return population

# Creates "genes" for indv randomly picked from all ascii values
def create_genes(gene_size=11):
    possible_genes = []
    for i in range(94):
        possible_genes.append(chr(i+32))
    genes = []
    for i in range(gene_size):
        genes.append(possible_genes[random.randint(0, 26)])
    return genes

# print function used to debug
def print_population(population):
    for indv in population.individual_list:
        print(indv.get_fitness())
        for i in indv.genes:
            print(f'{i}', end='')
        print()

# The algo itself
def gen_algo(target, population):
    new_indvs = []
    i = 1
    # Saves the fittest of the population for the new generation
    # fittest = get_fittest(population)
    fittest_list = get_ham_fittest_el(population, len(population.individual_list)*.1)
    new_indvs.extend(fittest_list)

    # Creates new indv by getting two fit indv from the tournament then crossing them over together.
    while i < len(population.individual_list):
        temp_indv_one = tournament(population)
        temp_indv_two = tournament(population)
        new_indv = crossover(temp_indv_one, temp_indv_two)
        # new_indv = crossover_slice(temp_indv_one, temp_indv_two)

        mutate(new_indv)
        new_indvs.append(new_indv)
        i += 1

    # creates new population, sets fitness and returns the population
    new_population = Population(new_indvs)
    # set_fitness(target, new_population)
    set_ham_fitness(target, new_population)
    return new_population


# Randomly selects indv for tournament then selects the strongest of them
def tournament(population):
    my_list = []
    for i in range(5):
        my_list.append(population.individual_list[random.randint(0, len(population.individual_list)-1)])
    tourny_pop = Population(my_list)
    # return get_fittest(tourny_pop)
    return get_ham_fittest(tourny_pop)


# Sets fitness determin on matching the target
def set_fitness(target, population):
    for indv in population.individual_list:
        indv.fitness = 0
        for i in range(len(indv.genes)):
            if indv.genes[i] == target[i]:
                indv.fitness += 1


# Hamming dist of two strings, need to revise code to use this style of fitness
def set_ham_fitness(target, population):
    for indv in population.individual_list:
        indv.fitness = 0
        for i in range(len(indv.genes)):
            if indv.genes[i] != target[i]:
                indv.fitness += 1

# Crosses over two indv to create one indv
def crossover(indv_one, indv_two):
    new_genes = []

    for i in range(len(indv_one.genes)):
        if i % 2 == 0:
            new_genes.append(indv_one.genes[i])
        else:
            new_genes.append(indv_two.genes[i])
    return Individual(new_genes, 0, 0)


    # Crosses over two indv to create one indv
def crossover_slice(indv_one, indv_two):
    new_genes = []
    length = len(indv_one.genes)
    rand = random.randint(0,length)
    


    return Individual(new_genes, 0, 0)

# Mutates the indv at a very low rate
def mutate(indv):
    possible_genes = []

    for i in range(94):
        possible_genes.append(chr(32+i))

    for i in range(len(indv.genes)):
        if random.random() <= 0.025:
            indv.genes[i] = possible_genes[random.randint(0, len(possible_genes)-1)]

# Main creates initial population, sets target and calls the genetic algo
def main():
    string = "Charles Darwin was right!"

    population = create_population(2000, string)
    # set_fitness(string, population)
    set_ham_fitness(string, population)
    generation = 0
    # while get_fittest(population).fitness < len(string):
    while get_ham_fittest(population).fitness != 0:

        generation += 1
        population = gen_algo(string, population)
        # fittest = get_fittest(population)
        fittest = get_ham_fittest(population)

        genes = fittest.genes
        for j in genes:
            print(j, end='')
        print()


    print(f"{generation} Generations ")

main()
