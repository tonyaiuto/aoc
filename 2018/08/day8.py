from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys

"""
The sleigh is much easier to pull than you'd expect for something
its weight. Unfortunately, neither you nor the Elves know which way
the North Pole is from here.

You check your wrist device for anything that might help. It seems
to have some kind of navigation system! Activating the navigation
system produces more bad news: "Failed to start navigation system.
Could not read software license file."

The navigation system's license file consists of a list of numbers
(your puzzle input). The numbers define a data structure which,
when processed, produces some kind of tree that can be used to
calculate the license number.

The tree is made up of nodes; a single, outermost node forms the
tree's root, and it contains all other nodes in the tree (or contains
nodes that contain nodes, and so on).

Specifically, a node consists of:

A header, which is always exactly two numbers:
The quantity of child nodes.
The quantity of metadata entries.
Zero or more child nodes (as specified in the header).
One or more metadata entries (as specified in the header).
Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
C, which has 1 child node (D) and 1 metadata entry (2).
D, which has 0 child nodes and 1 metadata entry (99).
The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?
"""

class Node(object):

  tag_no = 0

  def __init__(this, n_c, n_m):
    Node.tag_no += 1
    this.tag = Node.tag_no
    this.n_children = n_c
    this.n_meta = n_m
    this.children = []
    this.meta = []
    this.meta_sum = 0

  def __str__(this):
    ret = 'Node(%s, nc:%d [' % (this.tag, this.n_children)
    ret += ','.join([str(child.tag) for child in this.children])
    ret += '], nm:%d %s' % (this.n_meta, this.meta)
    return ret 

  @staticmethod
  def LoadNode(nv, pos):
    if pos >= len(nv):
      return None, 0
    node = Node(nv[pos], nv[pos+1])
    used = 2
    for ci in range(node.n_children):
      child, child_used = Node.LoadNode(nv, pos + used)
      node.children.append(child)
      used += child_used
    for mi in range(node.n_meta):
      node.meta.append(nv[pos+used+mi])
    node.meta_sum = sum(node.meta)
    used += node.n_meta
    return node, used

  @staticmethod
  def PrintTree(node, indent=0):
    i_str = ' ' * indent
    print('%s%s' % (i_str, node))
    for c in node.children:
      Node.PrintTree(c, indent+2)
 

def LoadNodes(inp):
  nv = [int(x) for x in inp.read().split(' ')]
  # print(nv)
  root, used = Node.LoadNode(nv, 0)
  if used != len(nv):
    raise ValueError('Only used %d values of %d' % (used, len(nv)))
  return root


# sum metadata
def part1(node):

  def sum_meta(node):
    ret = node.meta_sum
    for c in node.children:
      ret += sum_meta(c)
    return ret

  print('Sum meta=%d' % sum_meta(node))


"""
The second check is slightly more complicated: you need to find the
value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata
entries. So, the value of node B is 10+11+12=33, and the value of
node D is 99.

However, if a node does have child nodes, the metadata entries
become indexes which refer to those child nodes. A metadata entry
of 1 refers to the first child node, 2 to the second, 3 to the
third, and so on. The value of this node is the sum of the values
of the child nodes referenced by the metadata entries. If a referenced
child node does not exist, that reference is skipped. A child node
can be referenced multiple time and counts each time it is referenced.
A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

Node C has one metadata entry, 2. Because node C has only one child
node, 2 references a child node which does not exist, and so the
value of node C is 0.

Node A has three metadata entries: 1, 1, and 2. The 1 references
node A's first child node, B, and the 2 references node A's second
child node, C. Because node B has a value of 33 and node C has a
value of 0, the value of node A is 33+33+0=66.

So, in this example, the value of the root node is 66.

What is the value of the root node?
"""
def part2(node):

  def sum_meta(node):
    if not node.children:
      return node.meta_sum
    nc = len(node.children)
    ret = 0
    for c_i in node.meta:
      if 0 < c_i and c_i <= nc:
        ret += sum_meta(node.children[c_i - 1])
    return ret

  print('part2: sum meta=%d' % sum_meta(node))


if __name__ == '__main__':
  verbose = False
  iarg = 1
  if sys.argv[iarg] == '-v':
    verbose = True
    iarg += 1
  with open(sys.argv[iarg]) as inp:
    root = LoadNodes(inp)
  print(root)
  if verbose:
    Node.PrintTree(root)
  part1(root)
  part2(root)
