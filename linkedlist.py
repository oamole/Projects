#!/usr/bin/env python
# coding: utf-8

# # Linked Lists

# ## Overview
# 
# For this assignment you will complete the implementation of the linked list data structure (`LinkedList`) started during class, so that it supports (nearly) all the [common](https://docs.python.org/3.5/library/stdtypes.html#common-sequence-operations) and [mutable](https://docs.python.org/3.5/library/stdtypes.html#mutable-sequence-types) sequence operations.
# 
# Your implementation should make use of doubly-linked nodes (i.e., each containing a `prior` and `next` reference), an ever-present sentinel `head` node, and a "circular" topology (where the head and last nodes are, logically, neighbors). This setup should substantially simplify your implementation by reducing the edge cases and amount of iteration you have to perform.
# 
# Your implementation should *not* make use of the built-in Python list data structure (finally!).

# ## Implementation Details

# ### `LinkedList`
# 
# As with the previous assignment, we've partitioned the `LinkedList` methods you need to implement (and the test cases that follow) into seven categories:
# 
# 1. Subscript-based access
# 2. Stringification
# 3. Single-element manipulation
# 4. Predicates (True/False queries)
# 5. Queries
# 6. Bulk operations
# 7. Iteration
# 
# 
# ### Hints / Advice
# 
# While you will have to implement some of the methods from scratch — i.e., in terms of the new underlying linked storage mechanism — you should be able to reuse quite a few of your method implementations from the previous assignment (the array-backed list), providing you defined them in terms of other, lower-level methods. This may not always be the most efficient (e.g., loops that repeatedly make use of `__getitem__` to access succeeding elements are clear offenders), but while we recommend that you try to optimize for improved run-time efficiency it is not a grading criterion for this assignment.

# In[15]:


class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next  = next
    
    def __init__(self):
        self.head = LinkedList.Node(None) # sentinel node (never to be removed)
        self.head.prior = self.head.next = self.head # set up "circular" topology
        self.length = 0
        
        
    ### prepend and append, below, from class discussion
        
    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1
        
    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1
            
            
    ### subscript-based access ###
    
    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx
    
    def __getitem__(self, idx):
        assert(isinstance(idx, int))
        nidx=self._normalize_idx(idx)
        if nidx>self.length or self.length==0:
            raise IndexError
        temp=self.head.next
        for _ in range(nidx):
            temp=temp.next
        return temp.val
    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert(isinstance(idx, int))
        nidx=self._normalize_idx(idx)
        if nidx>self.length or self.length==0:
            raise IndexError
        temp=self.head.next
        for _ in range(nidx):
            temp=temp.next
        temp.val=value

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert(isinstance(idx, int))
        nidx=self._normalize_idx(idx)
        if nidx>self.length or self.length==0:
            raise IndexError
        temp=self.head.next
        for _ in range(nidx):
            temp=temp.next
        temp.prior.next=temp.next
        temp.next.prior=temp.prior
        self.length-=1
    

    ### stringification ###
    
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        return self.__repr__()

    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        # YOUR CODE HERE
        return '[' + ', '.join(str(x) for x in self) + ']'


    ### single-element manipulation ###
        
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        assert(isinstance(idx, int))
        nidx = self._normalize_idx(idx)

        if nidx == self.length:
            self.append(value)
        else:
            self.length += 1
            n = self.head.next
            for i in range(nidx):
                n = n.next
            newNode = LinkedList.Node(val=value, next=n, prior=n.prior)
            n.prior.next = n.prior = newNode
    
    def pop(self, idx=-1):
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        rv = self.__getitem__(idx)
        self.__delitem__(idx)
        return rv
    
    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        for i in range(self.length):
            if self[i] == value:
                self.__delitem__(i)
                return
        raise ValueError

    ### predicates (T/F queries) ###
    
    def __eq__(self, other):
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        if not isinstance(other, LinkedList):
            return False
        if len(other) != len(self):
            return False
        j = 0
        for i in other:
            if i != self[j]:
                return False
            j += 1
        return True
    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        for i in self:
            if value == i:
                return True
        return False

    ### queries ###
    
    def __len__(self):
        """Implements `len(self)`"""
        return self.length
    
    def min(self):
        """Returns the minimum value in this list."""
        min = self[0]
        for val in self:
            if val < min:
                min = val
        return min
    
    def max(self):
        """Returns the maximum value in this list."""
        max = self[0]
        for val in self:
            if val > max:
                max = val
        return max
    
    def index(self, value, i=0, j=None):
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        if j is None:
            for i in range(i, len(self)):
                if self[i] == value:
                    return i
        else:
            i = self._normalize_idx(i)
            j = self._normalize_idx(j)
            for i in range(i, j):
                if self[i] == value:
                    return i
        raise ValueError('Value Error found, Try Again Later')

    
    def count(self, value):
        """Returns the number of times value appears in this list."""
        count = 0
        for i in self:
            if i == value:
                count += 1
        return count

    
    ### bulk operations ###

    def __add__(self, other):
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those 
        of other."""
        assert(isinstance(other, LinkedList))
        rv = LinkedList()
        for i in self:
            rv.append(i)
        for j in other:
            rv.append(j)
        return rv
    
    def clear(self):
        """Removes all elements from this list."""
        for _ in range(self.length):
            self.__delitem__(-1)
        
    def copy(self):
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        rv = LinkedList()
        return self.__add__(rv)
    
    def extend(self, other):
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for i in other:
            self.append(i)
            
    ### iteration ###

    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        n = self.head.next
        while n is not self.head:
            yield n.val
            n = n.next


# In[16]:


# (6 points) test subscript-based access

from unittest import TestCase
import random

tc = TestCase()
data = [1, 2, 3, 4]
lst = LinkedList()
for d in data:
    lst.append(d)

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])
    
with tc.assertRaises(IndexError):
    x = lst[100]

with tc.assertRaises(IndexError):
    lst[100] = 0

with tc.assertRaises(IndexError):
    del lst[100]

lst[1] = data[1] = 20
del data[0]
del lst[0]

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])

data = [random.randint(1, 100) for _ in range(100)]
lst = LinkedList()
for d in data:
    lst.append(d)

for i in range(len(data)):
    lst[i] = data[i] = random.randint(101, 200)
for i in range(50):
    to_del = random.randrange(len(data))
    del lst[to_del]
    del data[to_del]

for i in range(len(data)):
    tc.assertEqual(lst[i], data[i])
    
for i in range(0, -len(data), -1):
    tc.assertEqual(lst[i], data[i])


# In[7]:


# (2 points) test stringification

from unittest import TestCase
tc = TestCase()

lst = LinkedList()
tc.assertEqual('[]', str(lst))
tc.assertEqual('[]', repr(lst))

lst.append(1)
tc.assertEqual('[1]', str(lst))
tc.assertEqual('[1]', repr(lst))

lst = LinkedList()
for d in (10, 20, 30, 40, 50):
    lst.append(d)
tc.assertEqual('[10, 20, 30, 40, 50]', str(lst))
tc.assertEqual('[10, 20, 30, 40, 50]', repr(lst))


# In[17]:


# (6 points) test single-element manipulation

from unittest import TestCase
import random

tc = TestCase()
lst = LinkedList()
data = []

for _ in range(100):
    to_ins = random.randrange(1000)
    ins_idx = random.randrange(len(data)+1)
    data.insert(ins_idx, to_ins)
    lst.insert(ins_idx, to_ins)

for i in range(100):
    tc.assertEqual(data[i], lst[i])

for _ in range(50):
    pop_idx = random.randrange(len(data))
    tc.assertEqual(data.pop(pop_idx), lst.pop(pop_idx))
    
for i in range(50):
    tc.assertEqual(data[i], lst[i])

for _ in range(25):
    to_rem = data[random.randrange(len(data))]
    data.remove(to_rem)
    lst.remove(to_rem)
    
for i in range(25):
    tc.assertEqual(data[i], lst[i])

with tc.assertRaises(ValueError):
    lst.remove(9999)


# In[18]:


# (4 points) test predicates
from unittest import TestCase
tc = TestCase()
lst = LinkedList()
lst2 = LinkedList()

tc.assertEqual(lst, lst2)

lst2.append(100)
tc.assertNotEqual(lst, lst2)

lst.append(100)
tc.assertEqual(lst, lst2)

tc.assertFalse(1 in lst)
tc.assertFalse(None in lst)

lst = LinkedList()
for i in range(100):
    lst.append(i)
tc.assertFalse(100 in lst)
tc.assertTrue(50 in lst)


# In[19]:


# (6 points) test queries

from unittest import TestCase
tc = TestCase()
lst = LinkedList()

tc.assertEqual(0, len(lst))
tc.assertEqual(0, lst.count(1))
with tc.assertRaises(ValueError):
    lst.index(1)

import random
data = [random.randrange(1000) for _ in range(100)]
for d in data:
    lst.append(d)

tc.assertEqual(100, len(lst))
tc.assertEqual(min(data), lst.min())
tc.assertEqual(max(data), lst.max())
for x in data:    
    tc.assertEqual(data.index(x), lst.index(x))
    tc.assertEqual(data.count(x), lst.count(x))

with tc.assertRaises(ValueError):
    lst.index(1000)

lst = LinkedList()
for d in (1, 2, 1, 2, 1, 1, 1, 2, 1):
    lst.append(d)
tc.assertEqual(1, lst.index(2))
tc.assertEqual(1, lst.index(2, 1))
tc.assertEqual(3, lst.index(2, 2))
tc.assertEqual(7, lst.index(2, 4))
tc.assertEqual(7, lst.index(2, 4, -1))
with tc.assertRaises(ValueError):
    lst.index(2, 4, -2)


# In[20]:


# (6 points) test bulk operations

from unittest import TestCase
tc = TestCase()
lst = LinkedList()
lst2 = LinkedList()
lst3 = lst + lst2

tc.assertIsInstance(lst3, LinkedList)
tc.assertEqual(0, len(lst3))

import random
data  = [random.randrange(1000) for _ in range(50)]
data2 = [random.randrange(1000) for _ in range(50)]
for d in data:
    lst.append(d)
for d in data2:
    lst2.append(d)
lst3 = lst + lst2
tc.assertEqual(100, len(lst3))
data3 = data + data2
for i in range(len(data3)):
    tc.assertEqual(data3[i], lst3[i])

lst.clear()
tc.assertEqual(0, len(lst))
with tc.assertRaises(IndexError):
    lst[0]

for d in data:
    lst.append(d)
lst2 = lst.copy()
tc.assertIsNot(lst, lst2)
tc.assertIsNot(lst.head.next, lst2.head.next)
for i in range(len(data)):
    tc.assertEqual(lst[i], lst2[i])
tc.assertEqual(lst, lst2)

lst.clear()
lst.extend(range(10))
lst.extend(range(10,0,-1))
lst.extend(data.copy())
tc.assertEqual(70, len(lst))

data = list(range(10)) + list(range(10, 0, -1)) + data
for i in range(len(data)):
    tc.assertEqual(data[i], lst[i])


# In[21]:


# (2 points) test iteration

from unittest import TestCase
tc = TestCase()
lst = LinkedList()

import random
data = [random.randrange(1000) for _ in range(100)]
lst = LinkedList()
for d in data:
    lst.append(d)
tc.assertEqual(data, [x for x in lst])

it1 = iter(lst)
it2 = iter(lst)
for x in data:
    tc.assertEqual(next(it1), x)
    tc.assertEqual(next(it2), x)


# In[ ]:




