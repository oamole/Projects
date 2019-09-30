#!/usr/bin/env python
# coding: utf-8

# # Heaps

# ## Overview
# 
# For this assignment you will start by modifying the heap data stucture implemented in class to allow it to keep its elements sorted by an arbitrary priority (identified by a `key` function), then use the augmented heap to efficiently compute the running median of a set of numbers.

# ## 1. Augmenting the Heap with a `key` function
# 
# The heap implementation covered in class is for a so-called "max-heap" — i.e., one where elements are organized such that the one with the maximum value can be efficiently extracted.
# 
# This limits our usage of the data structure, however. Our heap can currently only accommodate elements that have a natural ordering (i.e., they can be compared using the '`>`' and '`<`' operators as used in the implementation), and there's no way to order elements based on some partial or computed property.
# 
# To make our heap more flexible, you'll update it to allow a `key` function to be passed to its initializer. This function will be used to extract a value from each element added to the heap; these values, in turn, will be used to order the elements. 
# 
# We can now easily create heaps with different semantics, e.g.,
# 
# - `Heap(len)` will prioritize elements based on their length (e.g., applicable to strings, sequences, etc.)
# - `Heap(lambda x: -x)` can function as a *min-heap* for numbers
# - `Heap(lambda x: x.prop)` will prioritize elements based on their `prop` attribute
# 
# If no `key` function is provided, the default max-heap behavior should be used — the "`lambda x:x`" default value for the `__init__` method does just that. 
# 
# You will, at the very least, need to update the `_heapify` and `add` methods, below, to complete this assignment. (Note, also, that `pop_max` has been renamed `pop`, while `max` has been renamed `peek`, to reflect their more general nature.)

# In[16]:


class Heap:
    def __init__(self, key=lambda x:x):
        self.data = []
        self.key  = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2
        
    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2
    
    def heapify(self, idx=0):
        while True:
            l = Heap._left(idx)
            r = Heap._right(idx)
            maxidx = idx
            if l < len(self) and self.key(self.data[l]) > self.key(self.data[idx]):
                maxidx = l
            if r < len(self) and self.key(self.data[r]) > self.key(self.data[maxidx]):
                maxidx = r
            if maxidx != idx:
                self.data[idx], self.data[maxidx] = self.data[maxidx], self.data[idx]
                idx = maxidx
            else:
                break
            
    def add(self, x):
        self.data.append(x)
        i = len(self.data) - 1
        p = Heap._parent(i)
        while i > 0 and self.key(self.data[p]) < self.key(self.data[i]):
            self.data[p], self.data[i] = self.data[i], self.data[p]
            i = p
            p = Heap._parent(i)
        
    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self.heapify()
        return ret
    
    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


# In[17]:


# (1 point)

from unittest import TestCase
import random

tc = TestCase()
h = Heap()

random.seed(0)
for _ in range(10):
    h.add(random.randrange(100))

tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])


# In[18]:


# (1 point)

from unittest import TestCase
import random

tc = TestCase()
h = Heap(lambda x:-x)

random.seed(0)
for _ in range(10):
    h.add(random.randrange(100))

tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])


# In[19]:


# (2 points)

from unittest import TestCase
import random

tc = TestCase()
h = Heap(lambda s:len(s))

h.add('hello')
h.add('hi')
h.add('abracadabra')
h.add('supercalifragilisticexpialidocious')
h.add('0')

tc.assertEqual(h.data,
              ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])


# In[20]:


# (2 points)

from unittest import TestCase
import random

tc = TestCase()
h = Heap()

random.seed(0)
lst = list(range(-1000, 1000))
random.shuffle(lst)

for x in lst:
    h.add(x)

for x in range(999, -1000, -1):
    tc.assertEqual(x, h.pop())


# In[21]:


# (2 points)

from unittest import TestCase
import random

tc = TestCase()
h = Heap(key=lambda x:abs(x))

random.seed(0)
lst = list(range(-1000, 1000, 3))
random.shuffle(lst)

for x in lst:
    h.add(x)

for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x:abs(x))):
    tc.assertEqual(x, h.pop())


# ## 2. Computing the Running Median
# 
# The median of a series of numbers is simply the middle term if ordered by magnitude, or, if there is no middle term, the average of the two middle terms. E.g., the median of the series [3, 1, 9, 25, 12] is **9**, and the median of the series [8, 4, 11, 18] is **9.5**.
# 
# If we are in the process of accumulating numerical data, it is useful to be able to compute the *running median* — where, as each new data point is encountered, an updated median is computed. This should be done, of course, as efficiently as possible.
# 
# The following function demonstrates a naive way of computing the running medians based on the series passed in as an iterable.

# In[39]:


def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i%2 == 0:
            medians.append(values[i//2])
        else:
            medians.append((values[i//2] + values[i//2+1]) / 2)
    return medians


# In[40]:


running_medians_naive([3, 1, 9, 25, 12])


# In[41]:


running_medians_naive([8, 4, 11, 18])


# Note that the function keeps track of all the values encountered during the iteration and uses them to compute the running medians, which are returned at the end as a list. The final running median, naturally, is simply the median of the entire series.
# 
# Unfortunately, because the function sorts the list of values during every iteration it is incredibly inefficient. Your job is to implement a version that computes each running median in O(log N) time using, of course, the heap data structure!
# 
# ### Hints
# 
# - You will need to use two heaps for your solution: one min-heap, and one max-heap. 
# - The min-heap should be used to keep track of all values *greater than* the most recent running median, and the max-heap for all values *less than* the most recent running median — this way, the median will lie between the minimum value on the min-heap and the maximum value on the max-heap (both of which can be efficiently extracted)
# - In addition, the difference between the number of values stored in the min-heap and max-heap must never exceed 1 (to ensure the median is being computed). This can be taken care of by intelligently `pop`-ping/`add`-ing elements between the two heaps.

# In[52]:


def running_medians(iterable):
    minHeap = Heap()
    maxHeap = Heap(key=lambda x: -x)
    median = []
    for i in iterable:
            addNumber(i, minHeap, maxHeap)
            rebalance(minHeap, maxHeap)
            median.append(getMedians(minHeap, maxHeap))
    return median
def rebalance(minHeap, maxHeap):
        if len(maxHeap) > len(minHeap):
            biggerHeap = maxHeap
            smallerHeap = minHeap
        elif len(maxHeap) < len(minHeap):
            biggerHeap = minHeap
            smallerHeap = maxHeap
        else:
            return
        while (len(biggerHeap) - len(smallerHeap) >= 2):
            smallerHeap.add(biggerHeap.pop())
def getMedians(minHeap, maxHeap):
        if len(maxHeap) > len(minHeap):
            biggerHeap = maxHeap
            smallerHeap = minHeap
        elif len(maxHeap) < len(minHeap):
            biggerHeap = minHeap
            smallerHeap = maxHeap
        else:
            return (minHeap.peek() + maxHeap.peek()) / 2
    
        return biggerHeap.peek()
def addNumber(i, minHeap, maxHeap):
        if len(minHeap) == 0 or i < minHeap.peek():
            minHeap.add(i)
        else:
            maxHeap.add(i)
            


# In[62]:


# (2 points)

from unittest import TestCase
tc = TestCase()
tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))


# In[61]:


# (2 points)

import random
from unittest import TestCase
tc = TestCase()
vals = [random.randrange(10000) for _ in range(1000)]
tc.assertEqual(running_medians_naive(vals), running_medians(vals))


# In[60]:


# (4 points) MUST COMPLETE IN UNDER 10 seconds!

import random
from unittest import TestCase
tc = TestCase()
vals = [random.randrange(100000) for _ in range(100001)]
m_mid   = sorted(vals[:50001])[50001//2]
m_final = sorted(vals)[len(vals)//2]
running = running_medians(vals)
tc.assertEqual(m_mid, running[50000])
tc.assertEqual(m_final, running[-1])


# In[ ]:





# In[ ]:




