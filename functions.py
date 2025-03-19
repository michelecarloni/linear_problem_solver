import sys
from fractions import Fraction

from Problem import*




def convertFloatFraction(problem):
    vecCosts = problem.getVecCosts().copy()
    vecBounds = problem.getVecBounds().copy()
    matCoeff = problem.getMatCoeff().copy()
    
    # convert matCoeff
    fraction_matCoeff = [[Fraction(value).limit_denominator() for value in row] for row in matCoeff]
    
    # convert vecCosts
    fraction_vecCosts = [Fraction(value).limit_denominator() for value in vecCosts]
    
    # convert vecBounds
    fraction_vecBounds= [Fraction(value).limit_denominator() for value in vecBounds]
    
    problem.setVecCosts(fraction_vecCosts)
    problem.setVecBounds(fraction_vecBounds)
    problem.setMatCoeff(fraction_matCoeff)



def SBA(matCoeff, k):
    # find SBA
    SBA = []
    
    for i in range(0, len(matCoeff[0])-1):
        array = []
        for j in range(k, len(matCoeff)):
            array.append(matCoeff[j][i])
        if array.count(1) == 1 and all(num == 0 for num in array if num != 1):
            position = array.index(1)
            SBA.append(matCoeff[position][-1])
        else:
            SBA.append(0)
            
    # print SBA
    print('SBA:\t', end='')
    for i in range(0, len(SBA)):
        if i == 0:
            print(f'[ {SBA[i]}', end='\t')
        elif i == len(SBA)-1:
            print(f'{SBA[i]} ]')
        else:
            print(f'{SBA[i]},', end='\t')
    print()



# bland rule
def blandRule(matrix, value):
    
    posJ = [1]
    posI = [1]
    
    if value == 'min':
        
        for i in range(0, len(matrix[0])-1):
            if matrix[0][i] < 0:
                break
            
        posI[0] = i
        
    elif value == 'max':
        
        for i in range(0, len(matrix[0])-1):
            if matrix[0][i] > 0:
                break
            
        posI[0] = i
        
    
    # check infinite
    if value == 'max':
        for i in range(0, len(matrix[0])-1):
            count = 0
            for j in range(1, len(matrix)):
                if matrix[j][i] <= 0 :
                    count += 1
            if count == len(matrix)-1:
                print('INFINITE SOLUTION')
                sys.exit(0)

        
    for j in range(1, len(matrix)):
        
        if matrix[j][posI[0]] <= 0:
            continue
        else:
            min = float(matrix[j][-1]/matrix[j][posI[0]])
            posJ[0] = j
            break
        
    for j in range(1, len(matrix)):
        
        if matrix[j][posI[0]] <= 0:
            continue
        else:
            temp = float(matrix[j][-1]/matrix[j][posI[0]])
            if temp < min:
                min = temp
                posJ[0] = j
    
    return posI[0], posJ[0]





def printAllTable(matrix):
        
        for j in range(0, len(matrix)):
            for i in range(0, len(matrix[0])):
                print(matrix[j][i], end='\t')
            print()
        
        print('----------------------------------------------')


def checkAllNegative(vector):
    for i in range(0, len(vector)-1):
        if vector[i] > 0:
            return False
    
    return True


def checkEqualsArray(ar1, ar2):
    if len(ar1) != len(ar2):
        return False
    
    for val1, val2 in zip(ar1, ar2):
        if val1 != val2:
            return False
        
    return True