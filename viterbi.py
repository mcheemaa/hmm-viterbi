
import sys
import random
import math

import numpy
from collections import defaultdict 
import matplotlib.pyplot as plt 



def genDieNumbers(n, dieN, dieT):

    dieNum = dieN
    dieType = dieT

    start = dieType[0]
    die_num = []
    die_type = []

    loaded_die = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]

    for i in range(n):
        die_type.append(start)

        if (start == 'F'):
            roll = random.choices(dieNum)
        elif(start == 'L'):
            roll = random.choices(dieNum, loaded_die)

        finR = int(roll[0])

        die_num.append(finR)


        probS = random.random()

        if (start == 'F'):
            if (probS <= 0.01):
                start = 'L'
        elif (start == 'L'):
            if (probS <= 0.2):
                start = 'F'
        

    return die_num, die_type


def viterbi(seq, dieT):

    startP = [0.5, 0.5]
    transProb = [[0.99, 0.01], [0.2, 0.8]]
    emissionProb = [[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],[1/10, 1/10, 1/10, 1/10, 1/10, 1/2]]

    tab = numpy.zeros(shape = ( len(dieT), len(seq)))

    path = []
    finP = []

    for i in range(len(dieT)):
        tab[i][0] = math.log10(startP[i]) + math.log10(emissionProb[i][seq[0] - 1])  

    for j in range(1, len(seq)):
        for x in range(len(dieT)):
            other = 1
            if x == 1:
                other = 0
            temp = math.log10(emissionProb[x][seq[j] - 1]) +  max([math.log10(transProb[x][x]) + tab[x][j - 1], math.log10(transProb[other][x]) + tab[other][j - 1]])
            tab[x][j] = temp


    revSeq = seq[::-1]
    
    for i in range(len(revSeq)):
        maxState = None
        maxVal = - 10000000000

        v = (len(revSeq) - 1) - i

        for j in range(len(dieT)):
            tProb = 1
            
            if (v < len(revSeq) - 1):
                tProb = transProb[j][path[-1]]

            if ((tab[j][v] + tProb) > maxVal):
                maxVal = tab[j][v] + tProb
                maxState = j

        path.append(maxState)
        finP.append(str(maxState))


    return(finP[::-1])
    

def main():

    dieNum = ['1', '2', '3', '4', '5', '6']
    dieType = ['F', 'L']

    

    
    print("Ten Viterbi Predictions - Sequence Size 14 \n")
    for i in range(10):
        die_num, die_type = genDieNumbers(14, dieNum, dieType)

        path = viterbi(die_num, dieType)

        newP = [item.replace('1', 'L') for item in path]
        newP = [item.replace('0', 'F') for item in newP]

        print("Rolls:   " + str(die_num))
        print("Die:     " + str(die_type))
        print("Viterbi: " + str(newP) + "\n")


    trueP = 0
    trueN = 0
    falseP = 0
    falseN = 0

    finalScore = defaultdict(list) 

    print("Evaluating Effectiveness & Printing Graphs\n")

    for i in range(100, 2100, 100):

        tempAcc = []
        tempMCC = []

        for j in range(10):
            die_num, die_type = genDieNumbers(i, dieNum, dieType)

            path = viterbi(die_num, dieType)
            newP = [item.replace('1', 'L') for item in path]
            newP = [item.replace('0', 'F') for item in newP]

            for x in range(len(die_type)):
                
                if (die_type[x] == 'F'):
                    if (newP[x] == 'F'):
                        trueP = trueP + 1
                    else:
                        falseN = falseN + 1
                elif (die_type[x] == 'L'):
                    if (newP[x] == 'L'):
                        trueN = trueN + 1
                    else:
                        falseP = falseP + 1
            denVal = (trueP + falseN) * (trueP + falseP) * (trueN + falseP) * (trueN + falseN)
            if denVal == 0:
                denVal = 1
            accur = (trueP + trueN) / (trueN + trueP + falseN + falseP)
            mcc = ((trueP * trueN) - (falseP * falseN))/ (math.sqrt(denVal))
            
            tempAcc.append(accur)
            tempMCC.append(mcc)

        avgAcc = sum(tempAcc) / len(tempAcc)
        avgmcc = sum(tempMCC) / len(tempMCC)

        finalScore[i] = [avgAcc, avgmcc]

    act = []
    size = []
    mc = []
    
    for key in finalScore:
        size.append(key)
        act.append(finalScore[key][0])
        mc.append(finalScore[key][1])


    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Top - MCC & Bottom - ACC ')
    ax1.plot(size, mc, marker = 'x')
    ax2.plot(size, act, marker = 'x')

    plt.show() 

    print("Done !")


if __name__ == "__main__":
        main()

        



