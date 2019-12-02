import math as mt

class solution(Homogeneous, Particular):
    def __init__(self, m, c, k):
        self.homogeneous = Homogeneous.__init__(self, m, c, k,)
        self.particular = Particular.__init__(self,)

    def solve():
        pass    


class Homogeneous():
    def __init__(self, m, c, k,):
        self.m = m
        self.c = c
        self.k = k

    def abcFormulae(a, b, c):
        if -0.01 < a < 0.01:
            return (c/b, None, None, False)

        D = b*b - 4 * a * c
        C = -b/(2*a)

        if D < -0.01:
            if -0.01 < C < 0.01:
                C = 0
            return C, C, mt.sqrt(-D)/(2*a), True
        elif -0.01 < D < 0.01:
            return C, None, None, True
        else:
            return C +mt.sqrt(D)/(2*a), C -mt.sqrt(D)/(2*a), None, True

    def characteristicEquation(self,):
        eigenvalues = self.abcFormulae(self.m, self.c, self.k)
        for idx, value in enumerate(eigenvalues):
            if value == None:
                nondex = idx
                break
        # Subdivide the problem to the right analysis.
        choice = {}

        

    @property
    def ccrit(self,):
        return mt.sqrt(4*self.k*self.m)

    @property
    def dampinRatio(self,):
        return c/self.ccrit

    @property
    def naturalFrequency(self,):
        return mt.sqrt(k/m)

    @m.setter
    def m(self, m):
        self.__m = m

    @c.setter
    def c(self, c):
        self.__c = c

    @k.setter
    def k(self, k):
        self.__k = k

    
class Particular():
    def __init__(self,):
        pass