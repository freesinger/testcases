import random
import itertools
import numpy as np

operator = ['+', '-', '*', '/']
operator_set = []

def operatorSet():
    for i in range(len(operator)):
        for j in range(len(operator)):
            for k in range(len(operator)):
                temp = (operator[i], operator[j], operator[k])
                operator_set.append(temp)
            
def calculate(deck):
    for com in deck:
        print(com)

# def recursiveCal(deck):
    # for 

def main():
    decklist = np.array([random.randrange(1, 14) for i in range(4)])
    deck_comb = list(set(itertools.permutations(decklist)))
    operatorSet()
    print(operator_set)

if __name__ == '__main__':
    main()