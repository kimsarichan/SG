
import random 
import collections

Individu = collections.namedtuple('Individu', 'ind fitness')

class GA(object):
    def __init__(self, jum_pop=10, mut_rate=.3):
        self.jum_pop = jum_pop
        self.mut_rate = mut_rate

    def solve(self, fitness, initial_population, generation=10):
        """
        Main function of GA
        """
        current_generation = [Individu(ind, fitness(ind)) for ind in initial_population]
        print current_generation

    def _crossover(self, u, v):
        """
          n point crossover
        """
        n=(random.randint(0,8))
        point= [int(random.randint(0,8)) for i in range(n)]
        print n , point
        tem1=u.ind
        tem2=v.ind
        for p in point :
            tmp1=tem1[p:]+tem2[:p]
            tmp2=tem2[p:]+tem1[:p]
            tem1=tmp1
            tem2=tmp2
    
        id1=Individu(tem1, calculate_fitness(tem1))
        id2=Individu(tem2, calculate_fitness(tem2))
        return id1,id2
        
    def _mutation(self, ind):
        """
        Mutation function ..... coming soon
        """     

    def _selection(self, pop):
        """
        Selection function roulette wheel
        """     
        weight=sum(ind.fitness for ind in pop )
        n=random.uniform(0,weight)
        for ind in pop:
            if n < ind.fitness :
                return  ind
            n=n-ind.fitness
        return ind


    
if __name__ == "__main__":    
    def decode(ind):
        """
        Decode string individual into integer x,y (as function parameter)
        """
        mid = len(ind)/2
        x = int(ind[:mid],2)
        y = int(ind[mid:],2)
        return [x , y]

    def encode(x,y):
        """
        Encode two integers x,y into string as individual
        """
        bin_x = '{0:04b}'.format(x)
        bin_y = '{0:04b}'.format(y)
        return bin_x+bin_y

    def calculate_fitness(ind):
        """
        Calculate fitness of individual
        F(x,y) = 3x^2 + 2y^2 - 4x + y/2
        """
        val = decode(ind)
        x = val[0]
        y = val[1]
        f = 3*(x**2) + 2*(y**2) - (4*x) + (y*1.0/2)
        return 1 * 1.0 / f + .1
    ga = GA()

    #init population
    pop = ["".join([str(random.randint(0,1)) for _ in range(8)]) for _ in range(ga.jum_pop)]
    populasi=[Individu(ind,  calculate_fitness(ind)) for ind in pop]
    ga.solve(calculate_fitness, pop, generation=10)
    ind1=ga._selection(populasi)
    ind2=ga._selection(populasi)
    print ga._selection(populasi)
    print ga._crossover(ind1,ind2)


