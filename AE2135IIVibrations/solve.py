import math as mt
import numpy as np

class x:
    def __init__(self,*args, alternative = None):
        print("This class is not yet made, thus it is called x!")


class InitialValueConstants():
    def __init__(self,):
        # A class specifically pertaining the constants to solve the initial value problems
        self.__initialConstants = np.array((None, None))
        
    def checkIfNoneInitialValues(self,):
        if self.__initialConstants[0] == None or self.__initialConstants[1] == None:
            return True
        return False

    @property
    def initialConstants(self,):
        return self.__initialConstants

    @initialConstants.setter
    def initialConstants(self, input,):
        inBetween = np.array(input)
        if len(inBetween) != 2:
            raise ValueError("The solutionSpecifics should be a tuple containing constants, with lenght 2.")
        else:
            self.__initialConstants = inBetween


class ImaginaryConjugates(InitialValueConstants):
    def __init__(self, realPart = None, imaginaryPart= None, alternative = None, truncation = None):
        # Create two alternative ways to provide information. One logical, one useful in the homogeneous class.
        self.real = realPart
        self.imaginary = imaginaryPart

        # If the alternative method is used, this is something we should process, right?
        if realPart == None or imaginaryPart == None:
            if alternative == None:
                raise UnboundLocalError("At least provide either the (real and imaginary) part, or fill in the alternative. For imaginary conjugates.")
            
            _, self.real, self.imaginary, _ = alternative
        
        # Import the functions for the initial constants!
        super().__init__()

        # Truncate if it's approximately zero.
        if truncation == None:
            self.truncation = 0.01
        if -self.truncation < self.real <self.truncation:
            self.real = 0
            
    # Thé funtion that returns the actuals curves and bodies... <3
    def solveAtTime(self, t):
        if self.checkIfNoneInitialValues():
            raise ValueError("The initial values have not yet been calculated.")
        return mt.exp(self.real * t) * np.dot(self.initialConstants, np.array([mt.sin(t), mt.cos(t)] ))    

    # Solve the initial situation, if there is no time t1 is given, time t0 will be used.
    def initialSolve(self, x0, t0, v1, t1= None,):
        if t1 == None:
            t1= t0
        if not self.checkIfNoneInitialValues():
            raise PermissionError("There is already an initial problem specified.")
        
        A = np.array([[mt.sin(t0), mt.cos(t0)],
                      [self.real * mt.sin(t1) + mt.cos(t1), self.real * mt.cos(t1) - mt.sin(t1)]])
        y = np.array( [x0*mt.exp(-self.real*t0), v1*mt.exp(-self.real*t1)])
        self.initialConstants = np.linalg.lstsq(A, y, rcond=None)[0]


class RealEqual(InitialValueConstants):
    def __init__(self, real = None, alternative = None):
        # Two alternative ways to supply the information. One logical, one useful in the homogeneous class.
        self.real = real

        # Check whether the are actually filled in.
        if real == None:
            if alternative == None:
                raise UnboundLocalError("At least provide either the real solution, or fill in the alternative. For real but equal roots.")
            else:
                self.real = alternative[0]
        
        # Import the functions pertaining the initial constants.
        super().__init__()

    def solveAtTime(self, t):
        if self.checkIfNoneInitialValues():
            raise ValueError("The initial values have not yet been calculated.")
        return np.dot(np.array([mt.exp(self.real * t), t * mt.exp(self.real * t)]), self.initialConstants)

    def initialSolve(self, x0, t0, v1, t1 = None):
        if t1 == None:
            t1 = t0

        if not self.checkIfNoneInitialValues():
            raise PermissionError("There is already an initial problem specified.")

        A = np.array([[mt.exp(self.real * t0), t0 * mt.exp(self.real * t0)],
                      [self.real * mt.exp(self.real * t1), (self.real * t1 + 1) * mt.exp(self.real * t1)]])
        y = np.array([x0, v1])
        self.initialConstants = np.linalg.lstsq(A, y, rcond=None)[0]        


class RealDifferent(InitialValueConstants):
    def __init__(self, real1 = None, real2 = None, alternative = None):
        # Provide two ways to activate this class. The logical way and the useful way for the homogeneous class.
        self.real1 = real1
        self.real2 = real2

        if real1 == None or real2 == None:
            if alternative == None:
                raise UnboundLocalError("At least provide either the two real roots, or fill in the alternative. For real but different roots.")
            else:
                self.real1, self.real2, _, _ = alternative

        # Import the functions pertaining the initial constants:
        super().__init__()

    def solveAtTime(self, t):
        if self.checkIfNoneInitialValues():
            raise ValueError("The initial values have not yet been calculated.")
        return np.dot(self.initialConstants, np.array([mt.exp(self.real1 * t), mt.exp(self.real2 * t)]))

    def initialSolve(self, x0, t0, v1, t1 = None):
        if t1 == None:
            t1 = t0

        if not self.checkIfNoneInitialValues():
            raise PermissionError("There is already an initial problem specified.")

        A = np.array([[mt.exp(self.real1 * t0), mt.exp(self.real2 * t0)],
                      [self.real1 * mt.exp(self.real1* t1), self.real2 * mt.exp(self.real2 * t1)] ])
        y = np.array([x0, v1])
        self.initialConstants = np.linalg.lstsq(A, y, rcond=None)[0]


class Massless():
    def __init__(self, *args, **kwargs):
        raise ValueError("The mass of the system cannot be zero...")


class Homogeneous():
    def __init__(self, m, c, k, *args, **kwargs):
        # The systems accuracy values
        self.truncationError = 0.001

        # Some of the constants of the equation
        self.__m = m
        self.__c = c
        self.__k = k

        # Solve the homogeneous part
        self.solveTheHomogeneousEquation()


    def abcFormulae(self, a, b, c):
        # A simple ABC-formula solver for the roots.
        # The placement of the None-type in the returned tuple reveals the type of the roots.
        # As the input is expected to be of the type float or double, a simple truncation is
        # put in place to assure there will be no unbounded values.
        if -self.truncationError < a < self.truncationError:
            return c/b, c/b, c/b, None

        D = b*b - 4 * a * c
        C = -b/(2*a)

        if D <= -self.truncationError:
            if -self.truncationError < C < self.truncationError:
                C = 0
            return None, C, mt.sqrt(-D)/(2*a), None
        elif -self.truncationError < D < self.truncationError:
            return C, None, None, None
        else:
            return C +mt.sqrt(D)/(2*a), C -mt.sqrt(D)/(2*a), None, None


    def characteristicEquation(self,):
        # Solves the characteristic equation and returns a class of the right solution.
        eigenvalues = self.abcFormulae(self.__m, self.__c, self.__k)
        for idx, value in enumerate(eigenvalues):
            if value == None:
                typeOfSolution = idx
                break
        
        # What type of class-instance should we make?
        self.homogeneousSolutionInstance = self.SolutionclassWithEigenvalues()[typeOfSolution]

        # Lets make that one then!
        self.homogeneousSolutionInstance = self.homogeneousSolutionInstance(alternative = eigenvalues)


    def SolutionclassWithEigenvalues(self,):
        # Creates the classes and assigns the right values to them
        return {0: ImaginaryConjugates, 1: RealEqual, 2: RealDifferent, 3: Massless,}
    

    def homogeneousSolution(self, t,):
        return self.homogeneousSolutionInstance.solveAtTime(t)


    def solveTheHomogeneousEquation(self,):
        self.characteristicEquation()


    def homogeneousReset(self,):
        # Resets the specific solutionClass, als m, c or k has changed.
        self.solveTheHomogeneousEquation()

    # An entire load of variables, useful if you want to call or set them outside of the class!
    @property
    def ccrit(self,):
        return mt.sqrt(4*self.__k*self.__m)

    @property
    def dampingRatio(self,):
        return self.__c/self.ccrit

    @property
    def naturalFrequency(self,):
        return mt.sqrt(self.__k/self.__m)

    @property
    def m(self,):
        return self.__m

    @m.setter
    def m(self, m):
        self.__m = m
        self.homogeneousReset()

    @property
    def c(self,):
        return self.__c

    @c.setter
    def c(self, c):
        self.__c = c
        self.homogeneousReset()

    @property
    def k(self,):
        return self.__k

    @c.setter
    def k(self, k):
        self.__k = k
        self.homogeneousReset()


    
class Particular():
    def __init__(self, *args, **kwargs):
        pass


class Solution(Homogeneous, Particular):
    def __init__(self, m, c, k):
        super().__init__(m=m, c=c, k=k)

    def solve(self, t):
        return self.homogeneousSolution(t)

    def initialValueProblem(self, x0, t0, v1, t1 = None):
        if t1 == None:
            t1 = t0

        self.homogeneousSolutionInstance.initialSolve(x0, t0, v1, t1)
