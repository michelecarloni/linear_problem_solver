import numpy as np
from fractions import Fraction

class Problem:
    def __init__(self, funType, vecSize, matCoeff, vecCosts, vecBounds, vecSigns, vecVariableSigns):
        self.__funType = funType
        self.__vecSize = vecSize
        self.__matCoeff = matCoeff
        self.__vecCosts = vecCosts
        self.__vecBounds = vecBounds
        self.__vecSigns = vecSigns
        self.__vecVariableSigns = vecVariableSigns
        self.__matTot = []
        
    
    #GET METHODS
    def getFunType(self):
        return self.__funType
    
    def getVecSize(self):
        return self.__vecSize
        
    def getMatCoeff(self):
        return self.__matCoeff
        
    def getVecCosts(self):
        return self.__vecCosts
        
    def getVecBounds(self):
        return self.__vecBounds
        
    def getVecSigns(self):
        return self.__vecSigns
    
    def getVecVariableSigns(self):
        return self.__vecVariableSigns
    
    def getMatTot(self):
        return self.__matTot
    
    
    
    #SET METHODS
    def setFunType(self, funType):
        self.__funType = funType
        
    def setVecSize(self, vecSize):
        self.__vecSize = vecSize
        
    def setMatCoeff(self, matCoeff):
        self.__matCoeff = matCoeff
        
    def setVecCosts(self, vecCosts):
        self.__vecCosts = vecCosts
        
    def setVecBounds(self, vecBounds):
        self.__vecBounds = vecBounds
        
    def setVecSigns(self, vecSigns):
        self.__vecSigns = vecSigns
        
    def setVecVariableSigns(self, vecVariableSigns):
        self.__vecVariableSigns = vecVariableSigns
        
    def setMatTot(self, matTot):
        self.__matTot = matTot
        
        
        
        