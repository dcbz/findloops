#!/usr/bin/env python
# [ findloops.py ]
# [ nemo - 2016  ]
#
# Find loops in a CFG by traversing a dominator tree.
# The color_loops() function will highlight loops in the
# cfg using red for exit, blue for entry.
#

import dominator

from binaryninja import *
from collections import *

# COLORS FOR BLOCK HIGHLIGHT
blue = HighlightColor(red=10,green=20,blue=0xff)  # LOOP ENTRY
red  = HighlightColor(red=0xff,green=20,blue=0x1) # LOOP EXIT

# Stolen from ToB ;)
def get_LowLevelILBasicBlock_from_bb(func, inst):
        for block in func.low_level_il:
                for i in block:
                        if i.address == inst.address:
                                return block
        return None

class FindLoops:
	def get_loops(self):
		return self.__loops

	def color_block(self,target,color):
		#
		# Color the basic block based on its type.
		#
		if(not self.__loops):
			return None
		il_inst = ((self.__function).low_level_il)[target]
		il_block = get_LowLevelILBasicBlock_from_bb(self.__function, il_inst)
		il_block.set_user_highlight(color)

	def color_loops(self):
		#
		# Color loop entries and exits, blue and red.
		#
		if(not self.__loops):
			return None

		for l in self.__loops["self_loops"]:
			self.color_block(l,blue) # Color self loops blue
		for l in self.__loops["entries"]:
			self.color_block(l,blue) # Color entries
		for l in self.__loops["exits"]:
			self.color_block(l,red) # Color entries

	def __find_loops(self):
		#
		# Find loops in a dominator tree. Nodes which link 
		# to their own dominator are a loop.
		#
		self.__loops = {}
		self.__loops["self_loops"] = self.__nodes.nodes_with_selfloops() # self loops first.
		self.__loops["entries"] = []
		self.__loops["exits"] = []
		
		for block in self.__function.low_level_il:
			for e in block.outgoing_edges:
				if e.target in self.__domtree[block.start]:
					#print "[+] Loop start found @ 0x%xlx" % e.target
					self.__loops["entries"].append(e.target)
					#print "[+] Loop exit found @ 0x%lx" % block.start 
					self.__loops["exits"].append(block.start)
		return self.__loops

	def __init__(self,bv,f):
		self.__dom = dominator.Dominator(bv,f)
		self.__function = f
		self.__nodes = self.__dom.get_nodes() 
		self.__domtree = self.__dom.get_tree()
		self.__find_loops()

