#!/usr/bin/env python
# coding: utf-8

# # Ordered Hashtable
# 
# ## Overview
# 
# For this assignment you will update and complete the implementation of the hashtable data structure presented in class, which exposes an API mirroring that of the built-in Python `dict`. When iterating over its contents (supported by the `__iter__`, `keys`, `values`, and `items` methods), your updated implementation will also reflect the order in which key/value pairs were originally inserted into the hashtable. This will require that you implement the two-tiered list system described during lecture.
# 
# The operations you will implement are listed alongside their descriptions below (`h` refers to a hashtable):
# 
# | Operation | Description |
# |-----------|-------------|
# | `h[k]`&nbsp;`=`&nbsp;`v` | If `h` does not contain key `k`, a new `k`&rightarrow;`v` mapping is added, else the value for key `k` is updated to `v`. |
# | `h[k]`    | If `h` contains key `k`, the corresponding value is returned, else a `KeyError` is raised. |
# | `del`&nbsp;`h[k]` | If `h` contains key `k`, it is removed along with its value, else a `KeyError` is raised. Note that if `k` is re-inserted at some later point it is considered a new key (for ordering purposes). |
# | `k`&nbsp;`in`&nbsp;`h` | Returns `True` if key `k` is in `h`. |
# | `len(h)` | Returns the number of keys in `h`. |
# | `iter(h)` | Returns an iterator over all the keys in `h`, in the order they were added. |
# | `h.keys()` | (Same as above) |
# | `h.values()` | Returns an iterator over all the values in `h`, in the order they were added. |
# | `h.items()` | Returns an iterator over all the key/value pairs (as tuples) in `h`, in the order they were added. |
# 
# Your hashtable will be provided with the initial number of buckets on creation (i.e., in `__init__`); your implementation must heed this value, as there may be performance ramifications if it does not.

# In[ ]:


s = "hello world"


# In[ ]:


class OrderedHashtable:
    class Node:
        """This class is used to create nodes in the singly linked "chains" in
        each hashtable bucket."""
        def __init__(self, index, next=None):
            # don't rename the following attributes!
            self.index = index
            self.next = next
        
    def __init__(self, n_buckets=1000):
        # the following two variables should be used to implement the "two-tiered" 
        # ordered hashtable described in class -- don't rename them!
        self.indices = [None] * n_buckets
        self.entries = []
        self.count = 0
        
    def __getitem__(self, key):
        idx = hash(key) % len(self.indices)
        node = self.indices[idx]
        while node:
            if self.entries[node.index][0] == key:
                return self.entries[node.index][1]
            node = node.next
        raise KeyError
    
    def __setitem__(self, key, val):
        idx = hash(key) % len(self.indices)
        node = self.indices[idx]
        while node:
            if self.entries[node.index][0] == key:
                self.entries[node.index][1] = val
                return 
            node = node.next
        else:
            self.indices[idx] = OrderedHashtable.Node(self.count, self.indices[idx])
            self.entries.append([key,val])
            self.count += 1
    
    def __delitem__(self, key):
        idx = hash(key) % len(self.indices)
        node = self.indices[idx]
        if self.entries[node.index][0] == key:
            self.entries[node.index] = [None,None]
            self.indices[idx] = node.next
            self.count -= 1
            return
        while node.next:
            if self.entries[node.next.index][0] == key:
                self.entries[node.next.index] =  [None,None]
                node.next = node.next.next
                self.count -= 1
            else:
                node = node.next
    
        
    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False
        
    def __len__(self):
        return self.count
    
    def __iter__(self):
        for x in self.entries:
            if x[0] != None:
                yield x[0]
    def keys(self):
        return iter(self)
    
    def values(self):
        for x in self.entries:
            if x[0] != None:
                yield x[1]
                


                
    def items(self):
        for x in self.entries:
            if x[0] != None:
                yield x
                
    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'
            
    def __repr__(self):
        return str(self)


# In[ ]:


# (3 tests) Short tests

from unittest import TestCase
import random

tc = TestCase()

ht = OrderedHashtable(2)

for k, v in (('batman', 'bruce wayne'), ('superman', 'clark kent'), ('spiderman', 'peter parker')):
    ht[k] = v
    
tc.assertEqual(len(ht), 3)

tc.assertEqual(ht['superman'], 'clark kent')

tc.assertTrue('spiderman' in ht)
tc.assertFalse('iron man' in ht)

with tc.assertRaises(KeyError):
    ht['iron man']


# In[ ]:


# (3 points) Basic tests (insertion, fetch, count, chain-lengths)

from unittest import TestCase
import random

tc = TestCase()

class MyInt(int):
    def __hash__(self):
        """MyInts hash to themselves — already current Python default, 
        but just to ensure consistency."""
        return self
    
def ll_len(l):
    """Returns the length of a linked list with head `l` (assuming no sentinel)"""
    c = 0
    while l:
        c += 1
        l = l.next
    return c
    
ht = OrderedHashtable(10)
for i in range(25):
    ht[MyInt(i)] = i*2

tc.assertEqual(len(ht), 25)

for i in range(5):
    tc.assertEqual(ll_len(ht.indices[i]), 3)
    
for i in range(5, 10):
    tc.assertEqual(ll_len(ht.indices[i]), 2)

for i in range(25):
    tc.assertTrue(MyInt(i) in ht)
    tc.assertEqual(ht[MyInt(i)], i*2)


# In[ ]:


# (3 points) Update testing

from unittest import TestCase
import random

tc = TestCase()

ht = OrderedHashtable(100)
d = {}

for i in range(100):
    k, v = str(i), str(i*2)
    d[k] = v
    ht[k] = v
    
for j in range(0, 100, 2):
    k, v = str(i), str(i*3)
    d[k] = v
    ht[k] = v
    
for j in range(0, 100, 4):
    k, v = str(i), str(i*4)
    d[k] = v
    ht[k] = v
    
for i in range(100):
    tc.assertTrue(k in ht)
    tc.assertEqual(d[k], ht[k])


# In[ ]:


# (3 points) Deletion testing

from unittest import TestCase
import random

tc = TestCase()

ht = OrderedHashtable(100)
d = {}

for i in range(100):
    k, v = str(i), str(random.randrange(10000000, 99999999))
    d[k] = v
    ht[k] = v

for _ in range(50):
    k = str(random.randrange(100))
    if k in d:
        del d[k]
        del ht[k]

tc.assertEqual(len(ht), len(d))

for k,v in ht.items():
    tc.assertEqual(d[k], v)


# In[ ]:


# (4 points) Iteration order testing

from unittest import TestCase
import random

tc = TestCase()

ht = OrderedHashtable(1000)
l = [str(i) for i in range(0, 1000)]
random.shuffle(l)

for x in l:
    ht[x] = x

for _ in range(50):
    idx_to_del = random.randrange(len(l))
    val_to_del = l[idx_to_del]
    del ht[val_to_del]
    del l[idx_to_del]
    if random.randrange(2) == 0:
        l.append(val_to_del)
        ht[val_to_del] = val_to_del

for x, y in zip(l, ht):
    tc.assertEqual(x, y)


# In[27]:


# (4 points) Stress testing

from unittest import TestCase
from time import time
import random

tc = TestCase()

ht = OrderedHashtable(100000)
d = {}

start = time()

for _ in range(100000):
    k, v = str(random.randrange(100000)), str(random.randrange(10000000, 99999999))
    d[k] = v
    ht[k] = v
    
for k,v in d.items():
    tc.assertTrue(k in ht)
    tc.assertEqual(d[k], ht[k])
    
end = time()
print(end-start)
tc.assertLess(end-start, 1.5, 'Your implementation ran too slow!')


# In[ ]:




