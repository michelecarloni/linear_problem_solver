import sys
from fractions import Fraction
from functions import*

from Problem import*

# global variables
changeSigns = []    # array with 0s and 1s, th 1s indicate the variables with the sign changed, so we can restore them at the end
countA = 0    # count how many alphas I need to introduce in the ausiliar problem
vec_countA = []






def standardForm(problem):

    #SET EVERYTHING UP RIGHT
    funType = problem.getFunType()
    vecVariableSigns = problem.getVecVariableSigns().copy()
    vecSigns = problem.getVecSigns().copy()
    vecCosts = problem.getVecCosts().copy()
    matCoeff = problem.getMatCoeff().copy()
    vecBounds = problem.getVecBounds().copy()
    
    # change 'min' into 'max'
    if funType == 'min':
        """funType == 'max'"""
        
        for i in range(0, len(vecCosts)):
            vecCosts[i] = -vecCosts[i]
            
    # change variables signs from '<=' to '>='
    for i in range(0, len(vecVariableSigns)):
        
        if vecVariableSigns[i] == '<=':
            changeSigns.append(1)
            vecVariableSigns[i] = '>='
            
            vecCosts[i] = -vecCosts[i]
            
            for j in range(0, problem.getVecSize()[1]):
                matCoeff[j][i] = -matCoeff[j][i]
        else:
            changeSigns.append(0)
                
    # all the bounds need to be '>=':
    for j in range(0, problem.getVecSize()[1]):
        
        if vecBounds[j] < 0:
            vecBounds[j] = - vecBounds[j]
            
            if vecSigns[j] == '<=':
                vecSigns[j] = '>='
            elif vecSigns[j] == '>=':
                vecSigns[j] = '<='
        
            for i in range(0, len(matCoeff[0])):
                matCoeff[j][i] = -matCoeff[j][i]
            
    
    # create the standard problem
    global countA
    for j in range(0, len(vecSigns)):
        
        if vecSigns[j] == '>=':
            
            vecSigns[j] = '='
            vecCosts.append(0)
            vec_countA.append(1)
            countA += 1
            for k in range(0, len(vecSigns)):
                if k == j:
                    matCoeff[k].append(-1)
                else:
                    matCoeff[k].append(0)
                    
        elif vecSigns[j] == '<=':
            vecSigns[j] = '='
            vec_countA.append(0)
            vecCosts.append(0)
            for k in range(0, len(vecSigns)):
                if k == j:
                    matCoeff[k].append(1)
                else:
                    matCoeff[k].append(0)
                    
        elif vecSigns[j] == '=':
            vec_countA.append(1)
            countA+=1
                    
    vecCosts.append(0)
            
    
    # reset the variables with the new changes
    """problem.setFunType(funType)"""
    problem.setVecVariableSigns(vecVariableSigns)
    problem.setVecSigns(vecSigns)
    problem.setVecCosts(vecCosts)
    problem.setMatCoeff(matCoeff)
    problem.setVecBounds(vecBounds)
    
    
    #PRINT STANDARD PROBLEM
    print('STANDARD PROBLEM')
    
    for i in range(0, len(problem.getVecCosts())):
        print(problem.getVecCosts()[i], end='\t')
    print()
    
    for j in range(0, len(problem.getMatCoeff())):
        for i in range(0, len(problem.getMatCoeff()[0])):
            print(problem.getMatCoeff()[j][i], end='\t')
            
        print(problem.getVecBounds()[j])
    
    print('----------------------------------------------')
    print()
    
    for i in range(len(changeSigns), len(problem.getVecCosts())):
        changeSigns.append(0)
        
        

        

def pivot(matTot, value):
    posI, posJ = blandRule(matTot, value)
    print(f'posI: {posI}, posJ: {posJ}')
    divider = matTot[posJ][posI]
    row = []

    for i in range(0, len(matTot[posJ])):
        matTot[posJ][i] = matTot[posJ][i]/divider
        row.append(matTot[posJ][i])
        
    for j in range(0, len(matTot)):
        
        if j == posJ:
            continue
        
        aij = - matTot[j][posI]
        for k in range(0, len(row)):
            matTot[j][k] += row[k]*aij
            
    printAllTable(matTot)
    
    return matTot
     

def firstPhase(problem):
    print('--------------------- 1 PHASE ---------------------')
    print()
    print('Ausiliar problem')
    
    matCoeff = problem.getMatCoeff().copy()    
    vecBounds = problem.getVecBounds().copy()
    vecCosts = problem.getVecCosts().copy()
    vecSize = problem.getVecSize().copy()
        
    for i in range(0, len(vecCosts)):
        vecCosts[i] = 0
    vecCosts.pop()
    
    for i in range(0, countA):
        vecCosts.append(1)
    vecCosts.append(0)

    for j in range(0, len(matCoeff)):
        if vec_countA[j] == 1:
            for k in range(0, len(matCoeff)):
                if k == j:
                    matCoeff[k].append(1)
                    continue   
                matCoeff[k].append(0)
                
    for j in range(0, len(matCoeff)):
        matCoeff[j].append(vecBounds[j])

    matCoeff.insert(0, vecCosts)
    
    # PRINT ausiliar problem
    printAllTable(matCoeff)
        
    # find alphas
    list_alpha = []
    
    for i in range(len(matCoeff[0])-(countA+1), len(matCoeff[0])-1):
        array = []
        
        for j in range(1, len(matCoeff)):
            array.append(matCoeff[j][i])
        if array.count(1) == 1 and all(num == 0 for num in array if num != 1):
            array.insert(0, 0)
            position = array.index(1)
        
        print(f'position: {position}')
        
        row = []
        for i in range(0, len(matCoeff[0])-(countA+1)):
            row.append(-matCoeff[position][i])
        row.append(matCoeff[position][-1])
        list_alpha.append(row)
        
    
    # print alphas
    print(f'len: {len(list_alpha)}')
    for j in range(0, len(list_alpha)):
        print(f'a{j+1}:', end='\t')
        for i in range(0, len(list_alpha[0])):
            print(list_alpha[j][i], end= '\t')
        print()
        
    # new cost function
    list_sum = []
    for i in range(0, len(list_alpha[0])):
        sum = 0
        for j in range(0, len(list_alpha)):
            sum += list_alpha[j][i]
        list_sum.append(sum)
        
    z = list_sum[-1]
    list_sum.pop()
    
    for i in range(0, countA):
        list_sum.append(0)
    list_sum.append(z)
        
    # print new cost function
    print(f'z:', end='\t')
    for i in range(0, len(list_sum)):
        if list_sum[i] == 0:
            continue
        if list_sum[i] > 0:
            sumStr = '+' + str(list_sum[i])
        else:
            sumStr = str(list_sum[i])
            
        if i < vecSize[0]:
            print(f'{sumStr}*x{i+1}', end='\t')
        elif i == len(list_sum)-1:
            print(f'{sumStr}')
        else:
            print(f'{sumStr}*s{(i-vecSize[0])+1}', end='\t')
    print()
    
    del matCoeff[0]
    list_sum[-1] = -list_sum[-1]
    matCoeff.insert(0, list_sum)
    
    # ausiliar problem
    printAllTable(matCoeff)
    
    # pivot
    while checkEqualsArray(matCoeff[0], vecCosts) == False:
        
        """ASK STRONA"""
        
        # check if there is no solution
        count = 0
        for i in range(0, len(matCoeff[0])-1):
            if matCoeff[0][i] >= 0:
                count += 1
        if count == len(matCoeff[0])-1:
            print('THERE IS NO SBA')
            sys.exit(0)
        
        matCoeff = pivot(matCoeff, 'min')
        
    for i in range(0, countA):
        for j in range(0, len(matCoeff)):
            del matCoeff[j][-2]
            
    printAllTable(matCoeff)
    
    SBA(matCoeff, 0)
    
    """# find SBA
    SBA = []
    
    for i in range(0, len(matCoeff[0])-1):
        array = []
        for j in range(0, len(matCoeff)):
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
    print()"""
            
    # reset vecCosts
    vecCosts = problem.getVecCosts().copy()
    del matCoeff[0]
    matCoeff.insert(0, vecCosts)

    # find new vecCosts
    list_x = []

    for i in range(0, vecSize[0]):
        array = []
        for j in range(1, len(matCoeff)):
            array.append(matCoeff[j][i])
        if array.count(1) == 1 and all(num == 0 for num in array if num != 1):
            position = array.index(1)+1
            
            row = []
            for k in range(0, len(matCoeff[0])):
                if k == i: 
                    row.append(0)
                elif k == len(matCoeff[0])-1:
                    row.append(matCoeff[position][k])
                else:
                    row.append(-matCoeff[position][k])
            list_x.append(row)
        else:
            row = []
            for k in range(0, len(matCoeff[0])):
                if k == i:
                    row.append(1)
                else:
                    row.append(0)
            list_x.append(row)

    
    list_sum = []
    for j in range(0, len(list_x)):
        for i in range(0, len(list_x[0])):
            list_x[j][i] = list_x[j][i] * vecCosts[j]
    for i in range(0, len(list_x[0])):
        sum = 0
        for j in range(0, len(list_x)):
            sum += list_x[j][i]
        list_sum.append(sum)
        
    list_sum[-1] = -list_sum[-1]
    
    del matCoeff[0]
    matCoeff.insert(0, list_sum)
    
    print('NEW COSTS VECTOR')
    printAllTable(matCoeff)
            
    
    
    # set all the attributes of the problem
    vecCosts = matCoeff[0].copy()
    del matCoeff[0]
    matrix = matCoeff.copy()
    
    vecBounds = []
    
    for j in range(0, len(matrix)):
        vecBounds.append(matCoeff[j][-1])
        matCoeff[j].pop()
        
    problem.setVecCosts(vecCosts)
    problem.setVecBounds(vecBounds)
    problem.setMatCoeff(matCoeff)
    
            

    
    
    
    
def secondPhase(problem):
    print('--------------------- 2 PHASE ---------------------')
    print()
    matTot = problem.getMatCoeff().copy()    # only the matrix without costs and bounds
    vecBounds = problem.getVecBounds().copy()
    vecCosts = problem.getVecCosts().copy()    # all the costs include '-z'
    
    for j in range(0, len(matTot)):
        matTot[j].append(vecBounds[j])
    
    matTot.insert(0, vecCosts)


    while checkAllNegative(matTot[0]) == False:
        
        
        matTot = pivot(matTot, 'max')
        
    
    # set the right value of 'matTot' for the problem
    problem.setMatTot(matTot)
    
    

def printSolution(problem):
    
    funType = problem.getFunType()
    matTot = problem.getMatTot().copy()
    vecSize = problem.getVecSize().copy()
    if funType == 'min': 
        z = matTot[0][-1]
    else:
        z = -matTot[0][-1]
    
    del matTot[0]
    
    SBA = []
    
    for i in range(0, vecSize[0]):
        array = []
        for j in range(0, len(matTot)):
            array.append(matTot[j][i])
            
        if array.count(1) == 1 and all(num == 0 for num in array if num != 1):
            position = array.index(1)
            if changeSigns[i] == 1: 
                SBA.append(-matTot[position][-1])
            else:
                SBA.append(matTot[position][-1])
        else:
            SBA.append(0)
            
    print(f'The solution is\tz: {z}')
    
    for i in range(0, len(SBA)):
        if i == 0:
            print(f'[ {SBA[i]}',end='\t')
        elif i == len(SBA) - 1:
            print(f'{SBA[i]} ]')
        else:
            print(f'{SBA[i]},',end='\t')
    
    
    
    
    
    
    
    
    
    
def startSymplex(problem):
    
    convertFloatFraction(problem)
    
    standardForm(problem)
    
    if countA != 0:
        firstPhase(problem)
    else:
        matCoeff = problem.getMatCoeff()
        vecBounds = problem.getVecBounds()
        
        for j in range(0, len(matCoeff)):
            matCoeff[j].append(vecBounds[j])
        
        SBA(matCoeff, 1)
         
    # check first lines of code of this function
    secondPhase(problem)
    
    printSolution(problem)
    
    
    
    