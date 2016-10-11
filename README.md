This code uses the networkx python library (https://networkx.github.io) to 
generate an intermediate dominator list, then builds a dominator tree from it
and locates loops within the tree.

Sample usage is shown below:

>>> x = findloops.FindLoops(bv,f)
>>> x.color_loops()
>>> x.get_loops()
{'self_loops': [], 'exits': [114L, 203L], 'entries': [57L, 58L]}
