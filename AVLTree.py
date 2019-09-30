#!/usr/bin/env python
# coding: utf-8

# # AVLTree
# 
# ## Overview
# 
# In this notebook you will complete the following implementation of the balanced (AVL) binary search tree. Note that you should *not* be implementing the map-based API described in the plain (unbalanced) BSTree notebook — i.e., nodes in the AVLTree will only contain a single value.

# In[1]:


class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right
            
        def rotate_left(self):
            n = self.right
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n, self.left, n.right, n.left
        
        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None
            
    @staticmethod
    def rebalance(t):
       
        if AVLTree.Node.height(t.left) > AVLTree.Node.height(t.right):
            if AVLTree.Node.height(t.left.left) >= AVLTree.Node.height(t.left.right):
                t.rotate_right()
            else:
                t.left.rotate_left()
                t.rotate_right()
        else:
            if AVLTree.Node.height(t.right.right) >= AVLTree.Node.height(t.right.left):
                t.rotate_left()
            else:
                t.right.rotate_right()
                t.rotate_left()
            
    def add(self, val):
        assert(val not in self)
        def add_rec(node):
            if not node:
                return AVLTree.Node(val)
            elif val < node.val:
                node.left = add_rec(node.left)
            else:
                node.right = add_rec(node.right)
            if abs(AVLTree.Node.height(node.left) - AVLTree.Node.height(node.right)) >= 2:
                AVLTree.rebalance(node)
            return node
        self.root = add_rec(self.root)
        self.size += 1
        
    def __delitem__(self, val):
        assert(val in self)
        def del_rec(node):
            stack = [node]
            if val < node.val:
                node.left = del_rec(node.left)
            elif val > node.val:
                node.right = del_rec(node.right)
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    t = node.left
                    if not t.right:
                        node.val = t.val
                        node.left = t.left                        
                    else:
                        stack.append(t)
                        n = t
                        while n.right.right:
                            n = n.right
                            stack.append(n)
                        t = n.right
                        n.right = t.left
                        node.val = t.val
            while stack:
                n = stack.pop()
                if abs(AVLTree.Node.height(n.left) - AVLTree.Node.height(n.right)) >= 2:
                    AVLTree.rebalance(n)
            return node
                        
        self.root = del_rec(self.root)
        self.size -= 1
        
    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)
        
    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)
    
    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)


# In[2]:


# LL-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [3, 2, 1]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[3]:


# RR-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [1, 2, 3]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[4]:


# LR-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [3, 1, 2]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[5]:


# RL-fix (simple) test
# 3 points

from unittest import TestCase

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

tc = TestCase()
t = AVLTree()

for x in [1, 3, 2]:
    t.add(x)
    
tc.assertEqual(height(t.root), 2)
tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])


# In[6]:


# ensure key order is maintained after insertions and removals
# 15 points

from unittest import TestCase
import random

tc = TestCase()
vals = list(range(0, 100000000, 333333))
random.shuffle(vals)

t = AVLTree()
for x in vals:
    t.add(x)

for _ in range(len(vals) // 3):
    to_rem = vals.pop(random.randrange(len(vals)))
    del t[to_rem]

vals.sort()

for i,val in enumerate(t):
    tc.assertEqual(val, vals[i])


# In[7]:


# stress testing
# 15 points

from unittest import TestCase
import random

tc = TestCase()

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))
    
def check_balance(t):
    tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

t = AVLTree()
vals = list(range(1000))
random.shuffle(vals)
for i in range(len(vals)):
    t.add(vals[i])
    for x in vals[:i+1]:
        tc.assertIn(x, t, 'Element added not in tree')
    traverse(t.root, check_balance)

random.shuffle(vals)
for i in range(len(vals)):
    del t[vals[i]]
    for x in vals[i+1:]:
        tc.assertIn(x, t, 'Incorrect element removed from tree')
    for x in vals[:i+1]:
        tc.assertNotIn(x, t, 'Element removed still in tree')
    traverse(t.root, check_balance)


# In[ ]:





# In[ ]:




