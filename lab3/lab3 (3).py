from collections import namedtuple
from itertools import accumulate
from operator import xor
from typing import Callable
import random
from copy import deepcopy
import math

NUM_MATCHES = 20
NIM_SIZE = 10
NimPly = namedtuple('NimPly', 'row, num_objects')

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: NimPly) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


def computeNimSum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    # print(f'nimSum is: {result}')
    return result


def cookStatus(state: Nim) -> dict:
    cooked = dict()
    cooked["possibleMoves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["activeRowsNumber"] = sum(o > 0 for o in state.rows)
    cooked["totalElements"] = sum(state.rows)
    cooked["shortestRow"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longestRow"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    # cooked["nimSum"] = computeNimSum(state)

    bruteForce = list()
    for m in cooked["possibleMoves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        bruteForce.append((m, computeNimSum(tmp)))
    cooked["bruteForce"] = bruteForce

    return cooked


def humanAgent(state: Nim) -> NimPly:
    """ the player is a real human """
    selectedRow = int(input('Enter the index of the row: '))
    elementsToRemove = int(input('Enter the number of elements to remove: '))
    ply = NimPly(selectedRow, elementsToRemove)
    return ply


def randomAgent(state: Nim) -> NimPly:
    """ a totally random action """
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return NimPly(row, num_objects)


def expertSystem(state: Nim) -> NimPly:
    """ the agent related to the Task 3.1 """
    nimSum = computeNimSum(state)
    if nimSum != 0:
        # if the nimSum is not equal to 0 we have to remove objects in a way that the nimSum become equal to 0
        for i in state._rows:
            numberToBeRemained = 0 ^ nimSum ^ i
            if i > numberToBeRemained and (state.k is None or i-numberToBeRemained <= state.k):
                return NimPly(state._rows.index(i), i-numberToBeRemained)
    
    # the following part is related to the case in which the player who takes the last piece loses:    
    # crowdedRows = sum([i > 1 for i in state._rows])
    # if crowdedRows == 1:
    #     # when the number of rows with more than one element is equal to 1, it means that the action
    #     # we are going to do is the last arbitrary move and after that the result does not depend on 
    #     # the players actions
    #     for i in state._rows:
    #         if i > 1:
    #             elementsToRemove = i
    #             break
    #     selectedRow = state._rows.index(elementsToRemove)
    #     notEmptyRows = sum([i > 0 for i in state._rows])
    #     if notEmptyRows % 2 != 0:
    #         elementsToRemove -= 1

    # if we are here it means that either the nimSum is 0 or we could not remove a number of elements less than k
    # in order to achieve a 0 nimSum
    # in this case we just remove one element from a non-empty row
    for i in state._rows:
            if i != 0:
                return NimPly(state._rows.index(i), 1)


def evolvedRules(genome: list) -> Callable:
    """ the agent related to the Task 3.2 """
    def evolvable(state: Nim) -> NimPly:
        data = cookStatus(state)
        
        if random.random() < genome[0] and data["activeRowsNumber"] % 2 == 0:
            if random.random() < genome[1]:
                row = data["longestRow"]
            elif random.random() < genome[2]:
                row = data["shortestRow"]
            else:
                row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
        else:
            if random.random() < genome[3]:
                row = data["longestRow"]
            elif random.random() < genome[4]:
                row = data["shortestRow"]
            else:
                row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
        
        if random.random() < genome[5] and data["totalElements"] % 2 == 0:
            if random.random() < genome[6]:
                # remove the maximum elements from the selected row
                num_objects = state.rows[row] if (state.k is None or state.rows[row] <= state.k) else state.k
            elif random.random() < genome[7]:
                # remain a single element in the row
                num_objects = state.rows[row] - 1 if (state.k is None or state.rows[row] - 1 <= state.k) else state.k
            else:
                num_objects = math.floor(state.rows[row] * genome[8])
        else:
            if random.random() < genome[9]:
                # remove the maximum elements from the selected row
                num_objects = state.rows[row] if (state.k is None or state.rows[row] <= state.k) else state.k
            elif random.random() < genome[10]:
                # remain a single element in the row
                num_objects = state.rows[row] - 1 if (state.k is None or state.rows[row] - 1 <= state.k) else state.k
            else:
                num_objects = math.floor(state.rows[row] * genome[11])
        
        return NimPly(row, num_objects)

    return evolvable


def GA(populationSize: int, offspringSize: int, numGenerations: int) -> list:
    """genetic algorithm used to evolve the rules related to the evolvedRules agent"""
    Individual = namedtuple('Individual', ['genome', 'fitness'])
    population = list()

    def tournament(population: list) -> Individual:
        return max(random.choices(population, k=2), key=lambda i: i.fitness)
    

    def crossOver(genome1: list, genome2: list) -> list:
        cut = random.randint(0, len(genome1))
        return genome1[:cut] + genome2[cut:]


    def mutation(genome: list) -> list:
        point = random.randint(0, len(genome) - 1)
        if random.random() < 0.5:
            genome[point] = genome[point] + 0.1 if genome[point] < 0.9 else genome[point] - 0.5
        else:
            genome[point] = genome[point] - 0.1 if genome[point] > 0.1 else genome[point] + 0.5
        return genome


    for genome in [[round(random.random(), 3) for _ in range(12)] for _ in range(populationSize)]:
        fitness = evaluate(evolvedRules(genome), randomAgent)
        population.append(Individual(genome, fitness))

    for g in range(numGenerations):
        offspring = list()
        
        for i in range(offspringSize):
            if random.random() < 0.5:
                p = tournament(population)
                o = mutation(p.genome)
                f = evaluate(evolvedRules(o), randomAgent)
                offspring.append(Individual(o, f))
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = crossOver(p1.genome, p2.genome)
                f = evaluate(evolvedRules(o), randomAgent)
                offspring.append(Individual(o, f))
        
        population += offspring
        population = sorted(population, key=lambda i: -i.fitness)[:populationSize]

    return population[0].genome


def evaluate(agent1: Callable, agent2: Callable) -> float:
    """ evaluate agent1 with respect to agent2 """
    match = (agent1, agent2)
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = match[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def simulate(agent1: Callable, agent2: Callable) -> None:
    """ simulate a single custom match """
    match = (agent1, agent2)
    nim = Nim(NIM_SIZE)
    print(f'status: Initial board  -> {nim}')
    player = 0
    while nim:
        ply = match[player](nim)
        nim.nimming(ply)
        print(f'status: After {match[player].__name__} -> {nim}')
        player = 1 - player
    print(f"status: {match[player].__name__} won!")


if __name__ == "__main__":
    
    ## custom game:
    # simulate(humanAgent, randomAgent)

    ## Task 3.1:
    # resultHistory = []
    # for i in range(10):
    #     result = evaluate(expertSystem, randomAgent)
    #     resultHistory.append(result)
    # print(resultHistory)
    
    ## resultHistory: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    
    ## Task 3.2:
    # rules = GA(50, 10, 30)
    # print(rules)
    # rules = [0.126, 0.372, 0.27, 0.074, 0.948, 0.128, 0.203, 0.733, 0.516, 0.982, 0.523, 0.549]
    rules = [0.708, 0.431, 0.43000000000000005, 0.693, 0.649, 0.78, 0.458, 0.575, 0.047000000000000014, 0.938, 0.349, 0.148]
    resultHistory = []
    for i in range(10):
        result = evaluate(evolvedRules(rules), randomAgent)
        resultHistory.append(result)
    print(resultHistory)
    
    ## resultHistory: [0.55, 0.7, 0.8, 0.5, 0.9, 0.6, 0.65, 0.55, 0.75, 0.6]