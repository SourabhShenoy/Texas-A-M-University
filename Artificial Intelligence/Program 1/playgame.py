#!/usr/bin/python
import time
import getopt
import sys
import os
# Reference: http://aima.cs.berkeley.edu/python/games.html
class TreeNode(object):
	def __init__(self,utility=None,path=None):
		self.children = []
		self.path = []
		self.utility = utility
	
	def addChildren(self,node):
		self.children.append(node)

class Tree(object):
	def __init__(self,root=None):
		self.root=root

def printInfo():
	print "Incorrect Number of arguments\n", "Correct way of running is:\n","python gameplaying.py <Algo> <InputTree>\n"
	print "Algo can be minmax or alphabeta\n","Input should be of the form: ' ( 1 ( 5 7 ) 4 ) ) '. Surround by '' and have space before and after brackets\n"

# Reference: http://stackoverflow.com/questions/19749883/how-to-parse-parenthetical-trees-in-python

class Parse(object):
	def __init__(self,ipstring):
		self.tree = Tree()
		self.ipstring = ipstring
		self.ipstring=self.ipstring.split()
		
	def parseTree(self,ipstring):
		node=TreeNode()
		if ipstring[0] == '(':
			ipstring.pop(0)
			while ipstring[0] != ')':
				node.addChildren(self.parseTree(ipstring))
		elif ipstring[0] != '(' and ipstring[0]!= ')':
				node.utility = int(ipstring[0])
		ipstring.pop(0)
		return node

	def parseRoot(self):
		self.tree.root=self.parseTree(self.ipstring)
		return self.tree

class MinMax(object):
	def __init__(self,tree):
		self.tree=tree
		
	def getFinalValue(self):
		self.Minmax(self.tree.root,'max')
		return self.tree.root.path

	def Minmax(self, node, op):
		for n in node.children:
			if n.utility == None:
				self.Minmax(n,'max')
			if op == 'max':
				node.utility = self.op(node,'max')
			else:
				node.utility = self.op(node,'min')
	
	def op(self,node,op):
		path = None
		if op == 'min':
			utility=1e30000
			for i,c in enumerate(node.children):
				if c.utility < utility:
					utility = c.utility
					path = [i+1] + c.path
			if node.utility == None or node.utility > utility:
				node.path = path
				return utility
			return node.utility
		else:
			utility=-1e30000
			for i,c in enumerate((node.children)):
				if c.utility > utility:
					utility = c.utility
					path = [i+1] + c.path
			if node.utility == None or node.utility < utility:
				node.path = path
				return utility
			return node.utility
				
def main(argv):
	(options, args) = getopt.getopt(argv, '')
	if len(args) <= 1 or len(args) >= 3:
		printInfo()
		return
	
	algo = args[0]
	ip = args[1].replace('(',' ( ').replace(')',' ) ')
	
	string = Parse(ip)
	string = string.parseRoot()
	os.system('clear')
	if algo == 'minmax':
		mm=MinMax(string)
		res=mm.getFinalValue()
		print res
	elif method == 'alphabeta':
		pass
	else:
		printInfo()

if __name__ == '__main__':
	start_time = time.time()
	main(sys.argv[1:])
	print time.time() - start_time, "seconds\n"