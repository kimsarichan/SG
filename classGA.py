import random

class GA(object):
	"""docstring for ClassName"""
	def __init__(self, gen_lim=50, mut_rate=.02, cross_rate=.08):		
		self.gen_lim = gen_lim
		self.mut_rate = mut_rate
		self.cross_rate = cross_rate		

	def solve(self, pop, stagnant_lim = 200):
		gen_counter = 0
		stagnant_counter = 0
		while gen_counter<self.gen_lim and  stagnant_counter<stagnant_lim:
			stagnant_counter+=1
			pass

	def crossOver(u,v):
		"""
		n point crossOver
		"""
		front = [random.randint(0,len(u.kromosom)-1)]
		back = front
		while (back == front):
			back = random.randint(0,len(u.kromosom)-1)	
		if back < front:
			back, front = front, back

		temp1 = u.kromosom[:front] + v.kromosom[front:back] + u.kromosom[back:]
		temp2 = v.kromosom[:front] + u.kromosom[front:back] + v.kromosom[back:]

		u.kromosom = temp1
		v.kromosom = temp2
	
	def mutate(self,u):
		for i in range(len(kromosom)):
			n = random.uniform(0,1)
			if n <= self.mut_rate:
				if u.kromosom[1] == '1':
					u.kromosom[1] = '0'
				else:
					u.kromosom[1] = '1'


class Individu(object):
	"""docstring for ClassName"""
	def decode(self,ind):
		"""
		Decode string individual into integer x,y (as function parameter)
		"""
		mid = len(ind)/2
		x = int(ind[:mid],2)
		y = int(ind[mid:],2)
		return [x,y]
	def encode(self,x,y):
		"""
		Decode two integers x,y into string as individual
		"""
		bin_x = '{0:04b}'.format(x)
		bin_y = '{0:04b}'.format(y)
		return bin_x+bin_y

	def calculate_fitness(self,ind):
		"""
		calculate fitness of individual
		F(x,y) = 3x^2 + 2y^2 - 4x + y/2
		"""
		val = self.decode(ind)
		x = val[0]
		y = val[1]
		f= 3*(x**2) + 2*(y**2) - (4*x) + (y*1.0/2)
		return 1 * 1.0 / f + .1

	def __init__(self, jmlBit):		
		self.kromosom = "".join([str(random.randint(0,1)) for x in range(jmlBit)])
		self.fitness = self.calculate_fitness(self.kromosom)


class Populasi (object):
	def selectBest(self,current):
		if self.best is None:
			self.best = current
		elif self.best.fitness < current.fitness:
			self.best = current
		return current
	def inisialisasi_populasi(self,jum_pop):
		self.best = None
		self.pop = [self.selectBest(Individu(16)) for _ in range(jum_pop)]
		return self.pop

if __name__ == '__main__':			

	popAwal = Populasi() #inisiasi Populasi awal	
	print 'Masukkan jumlah populasi (ganjil):'
	popAwal.inisialisasi_populasi(int(raw_input())) #inisiasi jumlah populasi
	print 'Masukkan batas generasi:'
	n = int(raw_input())
	ga = GA()

	ga.solve(popAwal)

	print popAwal.best.kromosom
	print popAwal.best.fitness

