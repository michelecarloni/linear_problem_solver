from symplexAlgorithm import*

#GLOBAL VARIABLES

global funType

vecSize = []
matCoeff = []

vecCosts = []

vecBounds = []

vecSigns = []

vecVariableSigns = []

# print all the linear problem
def printProblem():
    global funType
    print(f'z:   {funType}: ',end='')
    
    i=0
    for cost in vecCosts:
        if cost >= 0:
            print('+', end='')
        print(f'{cost}*y{i+1} ', end='')
        
        i+=1
    print()
    print()
    
    j=0
    for column, sign, bound in zip(matCoeff, vecSigns, vecBounds):
        for i in range (0,vecSize[0]):
            if column[i] >= 0:
                print('+', end='')
            print(f'{column[i]}*x{j+1}{i+1} ', end='')
        
        j+=1
        print(f'{sign} {bound}')
        print()

#add values to my vector of signs
def vecSignsFun():
    global vecSigns
    
    print('choose from')
    print('>=    |    <=    |    =')
    
    i = 0
    while i < vecSize[1]:
        
        sign = input(f'{i+1}) sign: ')
        
        if sign != '>=' and sign != '<=' and sign != '=':
            print('error')
            continue
        else:
            i+=1
            vecSigns.append(sign)
    
    print('Here it is your SIGNS VECTOR')
    
    for sign in vecSigns:
        print(f'{sign}')

  
#add values to my vector of costs  
def vecCostsFun():
    global vecCosts
    
    print('INSERT THE COSTS VECTOR')
    print('use a space to separate all the elements (and include 0s)')
    
    while True:
        rowStr = input('costs: ')
        rowSplit = rowStr.split()
        vecCosts = list(map(float, rowSplit))
        if len(vecCosts) == vecSize[0]:
            break
        else:
            print('wrong size')
            continue
    
    print('Here it is your COSTS VECTOR')
    
    for cost in vecCosts:
        print(f'{cost} ', end='')
    print()
    

#add values to my vector of bounds
def vecBoundsFun():
    global vecBounds
    
    print('INSERT THE BOUNDS VECTOR')
    print('use a space to separate all the elements (and include 0s)')
    
    while True:
        rowStr = input('bounds: ')
        rowSplit = rowStr.split()
        vecBounds = list(map(float, rowSplit))
        if len(vecBounds) == vecSize[1]:
            break
        else:
            print('wrong size')
            continue
    
    print('Here it is your BOUNDS VECTOR')
    
    for bound in vecBounds:
        print(bound)
    
    
#add values to my coefficients matrix
def matCoeffFun():
    global matCoeff
    
    print('INSERT THE COEFFICIENTS MATRIX')
    print('use a space to separate all the elements (and include 0s)')
    
    print('Insert the width and the height of the matrix')
    var = int(input('WIDTH: '))
    vecSize.append(var)
    var = int(input('HEIGHT: '))
    vecSize.append(var)
    
    i=0
    while i < vecSize[1]:
        i+=1
        
        # take the row as an input. Each element is divided from the other with a space ' '
        rowStr = input((f'{i}) row: '))
        rowSplit = rowStr.split()
        
        # appen the width of the matrix to the vecSize
        if i == 1:
            vecSize.append(len(rowSplit))
        
        # add the list as an alement of matCoeff
        row = list(map(float, rowSplit))
        if len(row) == vecSize[0]:
            matCoeff.append(row)
        else:
            i-=1
            print(f'This row does not fit right in the matrix')
            
    #print the matrix
    print('Here it is your MATRIX OF COEFFICIENTS')
    print()
    
    for i in range (0,vecSize[1]):
        for j in range(0,vecSize[0]):
            if matCoeff[i][j]>=0:
                print('+', end='')
            print(f'{matCoeff[i][j]}*x{i+1}{j+1} ', end='')
            
        print()
        
def vecVariableSignsFun():
    global vecVariableSigns
    print('INSERT THE SIGNS OF THE VARIABLE')
    num = vecSize[0]
    
    i = 0
    while i < num:
        x = input(f'x{i+1}: ')
        
        if x == '<=' or x == '>=':
            i+=1
            vecVariableSigns.append(x)
        else:
            print('error')
            continue
        
    print('Here it is your SIGNS OF THE VARIABLES')
    print()

    for sign in vecVariableSigns:
        print(sign, end=' | ')
        



def intro():
    print('----------------------------------------------')
    print('| This program applies the symplex algorithm |')
    print('|       to solve every linear problem        |')
    print('----------------------------------------------')
    

def main():
    intro()
    
    while True:
        global funType
        funType = input('Insert the type of your funtion (min/max): ').lower()
        
        if funType == 'min' or funType == 'max':
            break
        else:
            print('error')
            continue
    
    matCoeffFun()
    vecBoundsFun()
    vecCostsFun()
    vecSignsFun()
    
    vecVariableSignsFun()
    
    printProblem()
    
    problem = Problem(funType, vecSize, matCoeff, vecCosts, vecBounds, vecSigns, vecVariableSigns)
    
    startSymplex(problem)
    

if __name__ == '__main__':
    main() 