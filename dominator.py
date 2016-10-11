#!/usr/bin/env python
# [              ]
# [ dominator.py ] 
# [ nemo 2016    ]
# [              ]
#
# Wrapper for networkx dominator code.
# Takes a binary ninja function object and
# converts it to a DiGraph() for processing.
# Builds a dominator tree from the immediate dominators
#

from binaryninja import *
from collections import *

import networkx as nx

class Dominator:
	def get_nodes(self):
		# Return the DiGraph()
		return self.__nodes

	def get_domfrontiers(self):
		# Return dominance frontiers list for function
		return nx.dominance_frontiers(self.__nodes,0) # return dominance frontiers

	def get_idom(self):
		# Return immediate dominators for function
		return nx.immediate_dominators(self.__nodes,0) # return idom

	def get_tree(self):
		# Build a dominator tree from the idom list.
		idom = self.get_idom() # get immediate dom array from nx
		dtree = {}
		for n in idom: # enumerate nodes
			dtree[n] = []
			ip = n
			while(True):
				ip = idom[ip]
		#		print "nextdom: %u" % ip
				dtree[n].append(ip)
				if(ip == 0):
					break
		return dtree

	def __init__(self,bv,f):
		#labels = {}
		self.__function = f
		self.__nodes = nx.DiGraph() # directional
		for block in f.low_level_il:
			self.__nodes.add_node(block.start)
			#labels[block.start] = "%u" % block.start#block.disassembly_text
			for e in block.outgoing_edges:
				self.__nodes.add_edges_from([(block.start,e.target)])


