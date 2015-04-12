import random

class GA(object):
	"""docstring for ClassName"""
	def __init__(self, gen_lim=50, mut_rate=.2, cross_rate=1):		
		self.gen_lim = gen_lim
		self.mut_rate = mut_rate
		self.cross_rate = cross_rate			

	def crossOver(self,u,v):
		"""
		n point crossOver
		"""
		n = random.random()
		if n > self.cross_rate: #checkin cross rate
			return

		front = random.randint(0,len(u.kromosom)-1)		
		back = front
		while (back == front):
			back = random.randint(0,len(u.kromosom)-1)	
		if back < front:
			back, front = front, back

		# print front
		# print back
		temp1 = u.kromosom[:front] + v.kromosom[front:back] + u.kromosom[back:]
		temp2 = v.kromosom[:front] + u.kromosom[front:back] + v.kromosom[back:]

		u.kromosom = temp1
		u.fitness = u.calculate_fitness()
		v.kromosom = temp2
		v.fitness = v.calculate_fitness()
	
	def mutate(self,u):
		temp = ""		
		for i in range(len(u.kromosom)):
			n = random.random()			
			if n <= self.mut_rate:	
				#print 'masuk'
				if u.kromosom[1] == '1':
					temp += '0'
				else:
					temp += '1'
			else:
				temp += u.kromosom[i]
		u.kromosom = temp
		u.fitness = u.calculate_fitness()

	def rouleteSelection(self, pop):		
		selectedChance = random.random()		
		for i in range(len(pop.individuChance)):			
			if selectedChance<pop.individuChance[i]:
				return pop.pop[i]

	def fillChildPopulation(self,childPop,parentPop):
		for x in xrange(childPop.jum_pop/2):			
			child1 = Individu()
			child1.kromosom = self.rouleteSelection(parentPop).kromosom #copy Kromosom parent 1, yg didapat dari roulete
			child2 = Individu()
			child2.kromosom = self.rouleteSelection(parentPop).kromosom #copy Kromosom parent 2, yg didapat dari roulete
			# print 'child1 ', child1.kromosom
			# print 'child2 ', child2.kromosom

			self.crossOver(child1,child2) #do cross over
			# print 'child1 ', child1.kromosom
			# print 'child2 ', child2.kromosom
			self.mutate(child1) #do mutation to first child
			self.mutate(child1) #do mutation to second child			
			childPop.pop.append(childPop.selectBest(child1))
			childPop.pop.append(childPop.selectBest(child2))

	def solve(self, parentPop, stagnant_lim = 500):
		gen_counter = 0
		stagnant_counter = 0
		while gen_counter<self.gen_lim and stagnant_counter<stagnant_lim:
			decodedValue = parentPop.best.decode(parentPop.best.kromosom)
			print 'Generasi #',gen_counter,':'
			print '    Best   : x= ', decodedValue[0], ' y= ', decodedValue[1]
			print '    Fitness: ',parentPop.best.fitness
			parentPop.createRoulete() # create roulete of parents
			childPop = Populasi(parentPop.jum_pop) # create empty population of children

			if parentPop.jum_pop%2==0:
				self.fillChildPopulation(childPop,parentPop) #fill child population	
				for x in xrange(childPop.jum_pop):
					if childPop.pop[x].fitness < parentPop.best.fitness: 
						"""
						change any individu of children pop with lower fitness than last gen best, to let the best survive
						"""
						childPop.pop[x] = parentPop.best
						childPop.selectBest(childPop.pop[x])
						break
			else:
				childPop.pop.append(childPop.selectBest(parentPop.best))
				self.fillChildPopulation(childPop,parentPop) #fill child population			

			if parentPop.best == childPop.best:
				stagnant_counter+=1
			else:
				stagnant_counter=0			
			gen_counter += 1
			parentPop = childPop
			
		return parentPop.best

		

class Individu(object):
	"""docstring for ClassName"""	
	def decode(self,kromosom):
		"""
		Decode string individual into integer x,y (as function parameter)
		"""
		mid = len(kromosom)/2
		x = int(kromosom[:mid],2)
		y = int(kromosom[mid:],2)
		return [x,y]
	def encode(self,x,y):
		"""
		Decode two integers x,y into string as individual
		"""
		bin_x = '{0:04b}'.format(x)
		bin_y = '{0:04b}'.format(y)
		return bin_x+bin_y

	def calculate_fitness(self):
		"""
		calculate fitness of individual
		F(x,y) = 3x^2 + 2y^2 - 4x + y/2
		"""
		val = self.decode(self.kromosom)
		x = val[0]
		y = val[1]
		f= 3*(x**2) + 2*(y**2) - (4*x) + (y*1.0/2)
		return 1 * 1.0 / (f + 0.01	)	

	def __init__(self, jmlBit=0):
		if jmlBit>0:			
			self.kromosom = "".join([str(random.randint(0,1)) for x in range(jmlBit)])
			self.fitness = self.calculate_fitness()		
		else:
			self.kromosom = ""
			self.fitness = 0


class Populasi (object):	
	def selectBest(self,current):
		if self.best is None:
			self.best = current
		elif self.best.fitness < current.fitness:
			self.best = current
		return current

	def inisialisasi_populasi(self):		
		self.pop = [self.selectBest(Individu(16)) for _ in range(self.jum_pop)]		
		return self.pop

	def createRoulete(self):
		totalFitness = sum([x.fitness for x in self.pop])				
		self.individuChance = []		
		for x in range(len(self.pop)):			
			if x == 0:
				self.individuChance.append(self.pop[x].fitness/totalFitness)
			else:
				self.individuChance.append(self.pop[x].fitness/totalFitness + self.individuChance[x-1])

	def __init__(self, jum_pop):
		self.jum_pop = jum_pop
		self.best = None
		self.pop = []
			
    	

if __name__ == '__main__':			
	
	print 'Masukkan jumlah populasi:'
	popAwal = Populasi(int(raw_input())) #inisiasi Populasi awal	
	popAwal.inisialisasi_populasi() #inisiasi jumlah populasi karena parent

	print 'Masukkan batas generasi:'
	n = int(raw_input())	

	ga = GA(n)
	print 'Masukkan batas stagnant:' #jalankan jika ingin set batas stagnant
	n = int(raw_input())	#jalankan jika ingin set batas stagnant

	bestIndividu = ga.solve(popAwal,n) #jalankan jika ingin set batas stagnant
	#bestIndividu = ga.solve(popAwal) #jalankan jika ingin batas stagnant default 500

	print 'Best Individu kromosom: ', bestIndividu.decode(bestIndividu.kromosom)
	print 'Best Individu fitness: ', bestIndividu.fitness

