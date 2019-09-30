#!/usr/bin/env python
# coding: utf-8

# # Preliminaries
# 
# All assignments for this class will be fetched, worked-on, and submitted via a dynamic in-browser Python development and testing environment known as the [Jupyter Notebook](http://jupyter.org/).
# 
# This first machine problem is intended to familiarize you with the environment and assignment retrieval/submission system, and to have you write some simple Python functions and test them using unit test cells, which will be found in all subsequent assignments.

# ## Fetching assignments
# 
# If you're reading this, then you're likely already familiar with the procedure for fetching an assignment. To recap:
# 
# - After logging in using your @hawk.iit.edu account, you'll either click "Start Server" or "My Server" to go to the Jupyter dashboard
# - From there, go to the "Assignments" tab, where you'll see any newly released assignments in the "Released assignments" area. You can fetch the files by clicking the "Fetch" button next to each assignment.
# - After an assignment has been fetched, you'll see it in the "Downloaded assignments" area, where you can expand the assignment to click on individual notebooks to open them up. You can also validate and submit your work here. Alternatively, you can also browse into an assignment folder from the "Files" tab and click on notebook files to open them up there.

# ## Exercise 1: Perfect Numbers
# 
# All of the lab notebooks you'll be working on for this class will come with a fair bit of skeleton code --- i.e., stubbed out classes and functions that you need to complete or modify to get working correctly.
# 
# In the cell below, for instance, you'll find a stubbed out function named `is_perfect`, which should return `True` if the number passed to it is a "perfect" number, and `False` otherwise.
# 
# A perfect number is a postive integer whose value is equal to the sum of its proper divisors (i.e., its factors excluding the number itself). 6 is the first perfect number, as its divisors 1, 2, and 3 add up to 6.
# 
# Complete the function by first deleting the comment "`# YOUR CODE HERE`" and the following `raise` statement, then filling in your own implementation.

# In[52]:


def is_perfect(n):
    x = 0
    for i in range(1,n):
        if n % i ==0:
            x+=i
    if x == n:
        return True 
    return False 
    


# Each exercise will also be accompanied by one or more *unit test* cells, each of which is meant to test some aspect of your implementation. When you run the unit test cell(s) after evaluating your implementation, you'll either find errors reported, which should help you identify what you need to fix, or they will complete silently, which means you've passed the test(s).
# 
# It's important that you ensure your implementation and test cell(s) are actually running to completion before moving on --- there's a big difference between a cell not producing an error and not completing! (A "`In [*]`" marker next to the cell means that it's still being evaluated by the interpreter.)
# 
# You should also note that we will often run *hidden tests* on our end to ensure that you didn't just hardcode solutions into your implementation. For this exercise, for instance, it's likely we'll be running your code against other values after submission in addition to the values we're testing below!

# In[51]:


# (3 points)
import unittest
tc = unittest.TestCase()

for n in (6, 28, 496):
    tc.assertTrue(is_perfect(n), '{} should be perfect'.format(n))

for n in (1, 2, 3, 4, 5, 10, 20):
    tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))

for n in range(30, 450):
    tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))


# ## Exercise 2: Multiples of 3 and 5
# 
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# 
# Complete the following function, which finds the sum of all the multiples of 3 or 5 below the argument `n`.

# In[1]:


def multiples_of_3_and_5(n):
    return sum(i for i in range(n) if i % 3==0 or i % 5==0)
    


# In[2]:


# (3 points)
import unittest
tc = unittest.TestCase()
tc.assertEqual(multiples_of_3_and_5(10), 23)
tc.assertEqual(multiples_of_3_and_5(500), 57918)
tc.assertEqual(multiples_of_3_and_5(1000), 233168)


# ## Exercise 3: Integer Right Triangles
# 
# Given a perimeter of 60, we can find two right triangles with integral length sides: [(10, 24, 26), (15, 20, 25)]. Complete the following function, which takes an integer `p` and returns a list of tuples (*a*, *b*, *c*) corresponding to the integral lengths of the sides of comforming right triangles. Each tuple should have $a \le b \lt c$, and the list should contain no duplicate solutions, and be sorted in order of ascending *a*.
# 
# Note that your solution should take care to limit the number of triangles it tests --- **your function must complete in under 3 seconds for all values of `p` used in the test cells below to earn credit.**

# In[3]:


def integer_right_triangles(p):
    general_list = []
    for a in range (1,p):
        for b in range (a,p):
            for c in range (b,p):
                if a+b+c == p and a**2+b**2 == c **2:
                    tupl = (a,b,c)
                    general_list.append(tupl)
    return general_list 
                
    


# In[4]:


# (1 point)
import unittest
tc = unittest.TestCase()
tc.assertEqual(integer_right_triangles(60), [(10, 24, 26), (15, 20, 25)])


# In[5]:


# (3 points)
import unittest
tc = unittest.TestCase()
tc.assertEqual(integer_right_triangles(100), [])
tc.assertEqual(integer_right_triangles(180), [(18, 80, 82), (30, 72, 78), (45, 60, 75)])
tc.assertEqual(integer_right_triangles(840), 
               [(40, 399, 401),
                (56, 390, 394),
                (105, 360, 375),
                (120, 350, 370),
                (140, 336, 364),
                (168, 315, 357),
                (210, 280, 350),
                (240, 252, 348)])


# ## Exercise 4: Simple ASCII Art
# 
# For this next exercise, you'll need to complete the function `gen_pattern`, which, when called with a string of length $\ge$ 1, will generate an ASCII art pattern of concentric diamonds using those characters. The following are examples of patterns returned by the function:
# 
#     > print(gen_pattern('X'))
#     
#     X
#     
#     > print(gen_pattern('XY'))
#     
#     ..Y..
#     Y.X.Y
#     ..Y..
#     
#     > print(gen_pattern('WXYZ'))
#     
#     ......Z......
#     ....Z.Y.Z....
#     ..Z.Y.X.Y.Z..
#     Z.Y.X.W.X.Y.Z
#     ..Z.Y.X.Y.Z..
#     ....Z.Y.Z....
#     ......Z......
#     
# Note that the function will *return* the pattern as a string (as opposed to printing it out), and so each line of the pattern should be separated by a newline, written as `'\n'` in Python. The second pattern above, as returned by `gen_pattern`, would be `''..Y..\nY.X.Y\n..Y..'`.
# 
# You ought to find the string [`join`](https://docs.python.org/3.6/library/stdtypes.html#str.join) and [`center`](https://docs.python.org/3.6/library/stdtypes.html#str.center) methods helpful in your implementation. They are demonstrated here:
# 
#     > '*'.join(['one', 'two', 'three'])
#     
#     'one*two*three'
#     
#     > '*'.join('abcde')
#     
#     'a*b*c*d*e'
#     
#     > 'hello'.center(11, '*')
#     
#     '***hello***'
#     
# Complete the `gen_pattern` function, below:

# In[6]:


def gen_pattern(chars):
    size  = len(chars) *4 -3
    sequence = []
    
    for i in range(len(chars)):
        first = chars[-1: -i -1:-1]
        last = chars[-i - 1:]
        output = first + last 
        sequence.append('.'.join(output).center(size,'.'))
    sequence += sequence[-2:: -1]
    print('\n'.join(sequence))
    return '\n'.join(sequence)


# In[7]:


# (2 points)
import unittest
tc = unittest.TestCase()
tc.assertEqual(gen_pattern('@'), '@')
tc.assertEqual(gen_pattern('@%'),
'''..%..
%.@.%
..%..''')


# In[8]:


# (2 points)
import unittest
tc = unittest.TestCase()
tc.assertEqual(gen_pattern('ABC'),
'''....C....
..C.B.C..
C.B.A.B.C
..C.B.C..
....C....''')
tc.assertEqual(gen_pattern('#####'),
'''........#........
......#.#.#......
....#.#.#.#.#....
..#.#.#.#.#.#.#..
#.#.#.#.#.#.#.#.#
..#.#.#.#.#.#.#..
....#.#.#.#.#....
......#.#.#......
........#........''')


# In[9]:


# (2 points)
import unittest
tc = unittest.TestCase()
tc.assertEqual(gen_pattern('abcdefghijklmnop'),
'''..............................p..............................
............................p.o.p............................
..........................p.o.n.o.p..........................
........................p.o.n.m.n.o.p........................
......................p.o.n.m.l.m.n.o.p......................
....................p.o.n.m.l.k.l.m.n.o.p....................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
....................p.o.n.m.l.k.l.m.n.o.p....................
......................p.o.n.m.l.m.n.o.p......................
........................p.o.n.m.n.o.p........................
..........................p.o.n.o.p..........................
............................p.o.p............................
..............................p..............................''')


# ## Submission
# 
# When you're ready to submit your work, make sure it's saved (you can click the disk icon in the menu bar), then go back to the "Assignments" tab and click "Submit" next to this assignment in the "Downloaded assignments" area. You can submit as many times as you like before the due date -- you'll see your submissions listed in the "Submitted assignments" area.
# 
# If you downloaded and worked on the notebook in your own local Jupyter Notebook server, please be sure to delete the old notebook (from the directory where it was placed when you retrieved the assignment) before uploading your completed one there for submission.
# 
# That's it for now!

# In[ ]:




