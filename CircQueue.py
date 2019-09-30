#!/usr/bin/env python
# coding: utf-8

# # Circular, Array-backed Queue

# ## Overview
# 
# For this assignment you will implement a circular, array-backed queue data structure.
# 
# In the following class, which you are to complete, the backing array will be created and populated with `None`s in the `__init__` method, and the `head` and `tail` indexes set to sentinel values (you shouldn't need to modify `__init__`). Enqueueing and Dequeueing items will take place at the tail and head, with `tail` and `head` tracking the position of the most recently enqueued item and that of the next item to dequeue, respectively. To simplify testing, your implementation should make sure that when dequeuing an item its slot in the array is reset to `None`, and when the queue is emptied its `head` and `tail` attributes should be set to `-1`.
# 
# Because of the fixed size backing array, the `enqueue` operation is defined to raise a `RuntimeError` when the queue is full — the same exception should be raised when `dequeue` is called on an empty queue.
# 
# Finally, the `resize` method will allow the array underlying the queue to be increased in size. It is up to you how to implement this (you can either leave the elements in their current positions, though this may require "unwrapping" elements, or you can simply move all elements towards the front of the array). You may assume that `resize` will only be called with a value greater than the current length of the underlying array.

# In[6]:


class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    

    def enqueue(self, val):
        if self.tail == len(self.data)-1: #if at last position, wrap
            if self.data[0] == None: 
                self.tail = 0
                self.data[self.tail] = val
            else:
                raise RuntimeError
            
        elif self.data[self.tail + 1] == None: #if the one after the current one is None, you can append
            self.tail +=1
            self.data[self.tail] = val
        else:
            raise RuntimeError
        
    def dequeue(self):
        if self.head == -1:
            self.head=0
        if self.data[self.head] != None:
            if self.head == len(self.data)-1: #if at last position, wrap
                to_ret = self.data[self.head]
                self.data[self.head] = None
                self.head = 0
            else:    
                to_ret = self.data[self.head]
                self.data[self.head] = None
                self.head +=1
            if self.empty():
                self.head = -1
                self.tail = -1
            return to_ret
        else:
            raise RuntimeError
    
    def resize(self, newsize):
        assert(len(self.data) < newsize)
        new = []
        
        for i in self:
            if i != None:
                 new.append(i)
                    
        self.head = 0
        self.tail = len(new) -1
        
        while len(new) < newsize:
            new.append(None)
        self.data = new
    
    def empty(self):
        for i in self.data:
            if i == None:
                pass
            else:
                return False
        return True
    def __bool__(self):
        return not self.empty()
    
    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        start = self.head
        if self.head > self.tail:
            right = len(self.data) - (self.head + 1)
            left = len(self.data) - right
            num = left + right
        elif self.head < self.tail:
            num = self.head - self.tail
        else: 
            num =0
        for i in range(num):
            if start == len(self.data)-1:
                if self.data[start] != None:
                    yield self.data[start]
                start =0
            else:
                if self.data[start] != None:
                    yield self.data[start]
                start +=1


# In[7]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(5)
tc.assertEqual(q.data, [None] * 5)

for i in range(5):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(5)

for i in range(5):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())


# In[8]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(10)

for i in range(6):
    q.enqueue(i)
    
tc.assertEqual(q.data.count(None), 4)

for i in range(5):
    q.dequeue()
    
tc.assertFalse(q.empty())
tc.assertEqual(q.data.count(None), 9)
tc.assertEqual(q.head, q.tail)
tc.assertEqual(q.head, 5)

for i in range(9):
    q.enqueue(i)

with tc.assertRaises(RuntimeError):
    q.enqueue(10)

for x, y in zip(q, [5] + list(range(9))):
    tc.assertEqual(x, y)
    
tc.assertEqual(q.dequeue(), 5)
for i in range(9):
    tc.assertEqual(q.dequeue(), i)

tc.assertTrue(q.empty())


# In[9]:


# (5 points)

from unittest import TestCase
tc = TestCase()

q = Queue(5)
for i in range(5):
    q.enqueue(i)
for i in range(4):
    q.dequeue()
for i in range(5, 9):
    q.enqueue(i)
    
with tc.assertRaises(RuntimeError):
    q.enqueue(10)

q.resize(10)

for x, y in zip(q, range(4, 9)):
    tc.assertEqual(x, y)
    
for i in range(9, 14):
    q.enqueue(i)

for i in range(4, 14):
    tc.assertEqual(q.dequeue(), i)
    
tc.assertTrue(q.empty())
tc.assertEqual(q.head, -1)


# In[ ]:





# In[ ]:




