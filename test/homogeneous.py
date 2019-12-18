import unittest
# This doesn't work yet, as the relevant classes are not yet imported...


class HomogeneousTestCase(unittest.TestCase):
    def setUp(self,):
        self.solution = Solution(1, 0, 1)
    
    def tearDown(self, ):
        self.solution = None

    def test_getNaturalFrequency(self,):
        self.assertEquals(1, self.solution.naturalFrequency)




if __name__ == "__main__":
    unittest.main()