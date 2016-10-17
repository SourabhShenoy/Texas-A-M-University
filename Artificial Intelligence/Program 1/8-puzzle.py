#!/usr/bin/python
import time
import sys
import copy
import operator
import getopt
import os

#Node stores the information like heuristic, the sequence of steps to reach current state, the current state and the level of the node
class Node:
	def __init__(self,currentState,heuristicVal=None,level=0,sequence=None):
		self.heuristicVal=heuristicVal
		self.currentState = currentState
		self.level = level
		if sequence == None:
			self.sequence = []
		else:
			self.sequence = sequence

#This is the parent class that has all common info used by all subclasses
class Master:
	def __init__(self, initialState, heuristic=None):
		self.initialNode = Node(initialState)
		self.heuristic = heuristic
		self.currentNode = self.initialNode
		self.visitedNodes = []
		self.visitedStates = {}
		key = ConvertToArray(initialState)
		self.visitedStates[key] = 1

#Method to display the board
	def display_board(self,State):
		print "-------------"
		print "| %i | %i | %i |" % (State[0][0], State[0][1], State[0][2])
		print "-------------"
		print "| %i | %i | %i |" % (State[1][0], State[1][1], State[1][2])
		print "-------------"
		print "| %i | %i | %i |" % (State[2][0], State[2][1], State[2][2])
		print "-------------"
	
#Method that gets all the possible moves for the blank tile. It can move left, up, down or right depending on it's location in the grid
	def getAllPossibleMoves(self):
		#return [i,j for i in range(0,3) for j in range (0,3) if self.currentNode.currentState[i][j] == 0 ]
		for i in range (0,3):
			for j in range(0,3):
				if self.currentNode.currentState[i][j] == 0:  #Location of the blank tile, numbered 0
					moves = []
					if i>=1:
						moves.append((i-1,j,'UP'))
					if i<=1:
						moves.append((i+1,j,'DOWN'))
					if j>=1:
						moves.append((i,j-1,'LEFT'))
					if j<=1:
						moves.append((i,j+1,'RIGHT'))
#					print moves,"\t", self.currentNode.currentState[i][j],"\n"
					return i,j,moves #Moves will have the list of possible moves. i,j has the i*j value of the blank tile

	def CalculateHeuristic(self,startState):
		sum = 0
		final = [[1,2,3],[8,0,4],[7,6,5]] #Desired State
		
		if self.heuristic == 'ntile':
			for i in range(0,3):
				for j in range (0,3):
					if final[i][j] != startState [i][j] and i!=1 and j!=1:  #Calculate how far the tiles are from desired state
							sum += 1
		elif self.heuristic == 'manhattan':
			#Reference from http://stackoverflow.com/questions/19770087/can-somebody-explain-in-manhattan-dstance-for-the-8-puzzle-in-java-for-me and http://www.csee.umbc.edu/courses/671/fall09/code/python/p8.py
			coordinates = { 0:(0,0), 1:(0,0), 2:(0,1),
							3:(0,2), 4:(1,2), 5:(2,2),
							6:(2,1), 7:(2,0), 8:(1,0)}  #Positions of the tiles in the desired state
			for i in range(0,3):
				for j in range(0,3):
					try:
						sum += abs(i-coordinates[startState[i][j]][0]) + abs(j-coordinates[startState[i][j]][1]) #Calculate how far the tiles are from desired state
					except KeyError:
						pass
		return sum

#BFS Search
class BFS(Master):
	def __init__(self, startState):
		Master.__init__(self, startState)
		print "\nInitial State:\n"
		self.display_board(startState)
		array = ConvertToArray(self.initialNode.currentState)
		self.visitedStates[array] = 0
		self.visitedNodes.insert(-1,self.initialNode) #-1, to insert at the end of the node
		
	def bfs(self):
		while len(self.visitedNodes) >= 1:
			PoppedNode = self.visitedNodes.pop(0)
			arrayPop = ConvertToArray(PoppedNode.currentState)
			self.visitedStates[arrayPop] = 0
#			print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#goal state reached
			if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#				print "Goal state reached!\n"
				print "\nFinal State:\n"
				self.display_board(PoppedNode.currentState)
				return PoppedNode.sequence
#if not found then add to the list and then repeat the steps
			self.currentNode = PoppedNode
			i_0,j_0,moves = self.getAllPossibleMoves()
			for i,j, move in moves:
				newState = copy.deepcopy(self.currentNode.currentState)
				newState[i_0][j_0] = newState[i][j]
				newState[i][j] = 0
				newNode = Node(newState,None,self.currentNode.level + 1,self.currentNode.sequence + [move])
				array = ConvertToArray(newState)
				try:
					self.visitedStates[array] += 1
				except KeyError:
					self.visitedNodes.insert(-1,newNode)
		
class DFS(Master):
	def __init__(self, startState):
		Master.__init__(self, startState)
		print "\nInitial State:\n"
		self.display_board(startState)
		array = ConvertToArray(self.initialNode.currentState)
		self.visitedStates[array] = 0
		self.visitedNodes.insert(0,self.initialNode)

	def dfs(self):
		while len(self.visitedNodes) >= 1:
			PoppedNode = self.visitedNodes.pop(0)
			arrayPop = ConvertToArray(PoppedNode.currentState)
			self.visitedStates[arrayPop] = 0
#			print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"

			if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#				print "Goal state reached!\n"
				print "\nFinal State:\n"
				self.display_board(PoppedNode.currentState)
				return PoppedNode.sequence
#goal state reached
			self.currentNode = PoppedNode
			#if not found then add to the list and then repeat the steps
			i_0,j_0,moves = self.getAllPossibleMoves()
			for i,j, move in moves:
				newState = copy.deepcopy(self.currentNode.currentState)
				newState[i_0][j_0] = newState[i][j]
				newState[i][j] = 0
				newNode = Node(newState,None,self.currentNode.level + 1,self.currentNode.sequence + [move])
				array = ConvertToArray(newState)
				try:
					self.visitedStates[array] += 1
				except KeyError:
					self.visitedNodes.insert(0,newNode)
		

class IDS(Master):
	def __init__(self, startState):
		Master.__init__(self, startState)
		print "\nInitial State:\n"
		self.display_board(startState)
		array = ConvertToArray(self.initialNode.currentState)
		self.visitedStates[array] = 0
		self.visitedNodes.insert(-1,self.initialNode)


	def ids(self,startState):
		depth = 1
		while 1:
			Master.__init__(self, startState)
			array = ConvertToArray(self.initialNode.currentState)
			self.visitedStates[array] = 0
			self.visitedNodes.insert(-1,self.initialNode)

			while len(self.visitedNodes) >= 1:
				PoppedNode = self.visitedNodes.pop(0)
				arrayPop = ConvertToArray(PoppedNode.currentState)
				self.visitedStates[arrayPop] = 0
	#			print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#goal state reached
				if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
	#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
	#				print "Goal state reached!\n"
					print "\nFinal State:\n"
					self.display_board(PoppedNode.currentState)
					return PoppedNode.sequence
#if not found then add to the list and then repeat the steps
				self.currentNode = PoppedNode
				if self.currentNode.level < depth:
					i_0,j_0,moves = self.getAllPossibleMoves()
					for i,j, move in moves:
						newState = copy.deepcopy(self.currentNode.currentState)
						newState[i_0][j_0] = newState[i][j]
						newState[i][j] = 0
						newNode = Node(newState,None,self.currentNode.level + 1,self.currentNode.sequence + [move])
						array = ConvertToArray(newState)
						try:
							self.visitedStates[array] += 1
						except KeyError:
							self.visitedNodes.insert(-1,newNode)
			depth += 1
		print depth

class Greedy(Master):
	def __init__(self, startState, heuristic):
		Master.__init__(self, startState, heuristic)
		print "\nInitial State:\n"
		self.display_board(startState)
		array = ConvertToArray(self.initialNode.currentState)
		self.visitedStates[array] = 0
		self.visitedNodes.insert(0,self.initialNode)
		self.initialNode.heuristicVal = self.CalculateHeuristic(startState)
		
	def greedy(self):
		while len(self.visitedNodes) >= 1:
			PoppedNode = self.visitedNodes.pop(0)
			arrayPop = ConvertToArray(PoppedNode.currentState)
			self.visitedStates[arrayPop] = 0
#			print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#goal state reached
			if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#				print "Goal state reached!\n"
				print "\nFinal State:\n"
				self.display_board(PoppedNode.currentState)
				return PoppedNode.sequence

			self.currentNode = PoppedNode
			#if not found then add to the list and then repeat the steps
			i_0,j_0,moves = self.getAllPossibleMoves()
			for i,j, move in moves:
				newState = copy.deepcopy(self.currentNode.currentState)
				newState[i_0][j_0] = newState[i][j]
				newState[i][j] = 0
#				print self.CalculateHeuristic(newState), "\n"
				newNode = Node(newState,self.CalculateHeuristic(newState),self.currentNode.level + 1,self.currentNode.sequence + [move])
				array = ConvertToArray(newState)
				try:
					self.visitedStates[array] += 1
				except KeyError:
					self.visitedNodes.insert(0,newNode)
					self.visitedStates[array] = 0
			self.visitedNodes.sort(key=operator.attrgetter('heuristicVal'))


		
class IDAStar(Master):
	def __init__(self, startState, heuristic):
		self.startState = startState
		Master.__init__(self, startState, heuristic)
		print "\nInitial State:\n"
		self.display_board(startState)
		self.initialNode.heuristicVal = self.CalculateHeuristic(startState)
		self.visitedNodes.insert(0,self.initialNode)



	def idastar(self,startState,heuristic):
		depth = 1
		while 1:
			Master.__init__(self, self.startState, self.heuristic)
			self.initialNode.heuristicVal = self.CalculateHeuristic(self.startState)
			self.visitedNodes.insert(0,self.initialNode)

			while len(self.visitedNodes) >= 1:
				PoppedNode = self.visitedNodes.pop(0)
#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#goal state reached
				if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
	#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
	#				print "Goal state reached!\n"
					print "\nFinal State:\n"
					self.display_board(PoppedNode.currentState)
					return PoppedNode.sequence
#if not found then add to the list and then repeat the steps
				self.currentNode = PoppedNode
				if self.currentNode.heuristicVal <= depth:
					i_0,j_0,moves = self.getAllPossibleMoves()
					for i,j, move in moves:
						newState = copy.deepcopy(self.currentNode.currentState)
						newState[i_0][j_0] = newState[i][j]
						newState[i][j] = 0
		#				print self.CalculateHeuristic(newState), "\n"
						newLevel = self.currentNode.level + 1
						newNode = Node(newState,self.CalculateHeuristic(newState) + newLevel,newLevel,self.currentNode.sequence + [move])
						self.visitedNodes.insert(0,newNode)
					self.visitedNodes.sort(key=operator.attrgetter('heuristicVal'))

			depth += 1
			
#A Star Algorithm using both heuristics
class AStar(Master):
	def __init__(self, startState, heuristic):
		Master.__init__(self, startState, heuristic)
		print "\nInitial State:\n"
		self.display_board(startState)
		self.initialNode.heuristicVal = self.CalculateHeuristic(startState)
		self.visitedNodes.insert(0,self.initialNode)

	def astar(self):
		while len(self.visitedNodes) >= 1:
			PoppedNode = self.visitedNodes.pop(0)
#			print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#goal state reached
			if PoppedNode.currentState == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]:
#				print PoppedNode.currentState, "\t", PoppedNode.sequence ,"\n"
#				print "Goal state reached!\n"
				print "\nFinal State:\n"
				self.display_board(PoppedNode.currentState)
				return PoppedNode.sequence

			self.currentNode = PoppedNode
			#if not found then add to the list and then repeat the steps
			i_0,j_0,moves = self.getAllPossibleMoves()
			for i,j, move in moves:
				newState = copy.deepcopy(self.currentNode.currentState)
				newState[i_0][j_0] = newState[i][j]
				newState[i][j] = 0
#				print self.CalculateHeuristic(newState), "\n"
				newLevel = self.currentNode.level + 1
				newNode = Node(newState,self.CalculateHeuristic(newState) + newLevel,newLevel,self.currentNode.sequence + [move])
				self.visitedNodes.insert(0,newNode)
			self.visitedNodes.sort(key=operator.attrgetter('heuristicVal'))


#Similar to a case state.
def searchMethod(obj,num):
	search = {  0 : 'obj.bfs()',
				1 : 'obj.dfs()',
				2 : 'obj.ids()',
				3 : 'obj.greedy()',
				4 : 'obj.astar()',
				5 : 'obj.idastar()',
	}
	
	method = search.get(num)
	return eval(method)

def main(argv):
	(options, args) = getopt.getopt(argv, '')
	if len(args) <= 1 or len(args) > 3:
		printInfo()
		exit(0)
	if len(args[1]) != 9:
		printFormat()
		exit(0)
	gameMatrix = ConvertToMatrix(args[1].strip())
	result = []
	os.system('clear')
	if len(args) == 2: #Uninformed Search
		if args[0].lower() == 'bfs':
			bfs=BFS(gameMatrix)
			result = searchMethod(bfs,0)
		elif args[0].lower() == 'dfs':
			dfs=DFS(gameMatrix)
			result = searchMethod(dfs,1)
		elif args[0].lower() == 'ids':
			ids=IDS(gameMatrix)
			result = ids.ids(gameMatrix)
		else:
			print "Enter correct search method"
			exit(0)
	else: #Informed search
		if args[0].lower() == 'greedy' and (args[2].lower() == 'ntile' or args[2].lower() == 'manhattan'):
			greedy = Greedy(gameMatrix, args[2].lower())
			result = searchMethod(greedy,3)
		elif args[0].lower() == 'astar' and (args[2].lower() == 'ntile' or args[2].lower() == 'manhattan'):
			astar = AStar(gameMatrix, args[2].lower())
			result = searchMethod(astar,4)
		elif args[0].lower() == 'idastar' and (args[2].lower() == 'ntile' or args[2].lower() == 'manhattan'):
			idastar = IDAStar(gameMatrix, args[2].lower())
			result = idastar.idastar(gameMatrix,args[2].lower())
		else:
			print "Enter Correct Method/Heuristic"
			exit(0)
	return result
	
	
#Convert from 2DMatrix to Array to set visited in the dictionary
def ConvertToMatrix(array):
	TwoDMatrix = []
	for i in range(0,3):
		row=[]
		for j in range(0,3):
			row.append(int(array[i*3+j]))
		TwoDMatrix.append(row)
	return TwoDMatrix


#Convert from array to 2DMatrix to perform computation
def ConvertToArray(TwoDMatrix):
	array = ''
	for i in TwoDMatrix:
		for j in i:
			array += str(j)
	return array

#Information to the user
def printFormat	():
	print "The second argument has to have exactly 9 numbers ranging from 0 to 8, each appearing only once!"

#Information for user
def printInfo():
	print "Incorrect Number of arguments\n", "Correct way of running is:\n","python 8-puzzle.py <Algo> <Input> [Heuristic (For informed)]\n"
	print "Algo can be bfs,dfs,ids,greedy,astar,idastar\n","Input should be similar to: 123456780\n","Heuristic can be ntile, manhattan\n"

#Result is returned by main. Print it to the output
if __name__ == "__main__":
	start_time = time.time()
	endState = main(sys.argv[1:])
	if endState:
		print "\n",endState
		print "\n",len(endState), "Moves\n"
	else:
		print "No Solution\n"
	print time.time() - start_time, "seconds\n"
