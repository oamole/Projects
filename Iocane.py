#!/usr/bin/env python
# coding: utf-8

# # Iocane Powder
# 
# ## Overview
# 
# > Man in Black: All right. Where is the poison? The battle of wits has begun. It ends when you decide and we both drink, and find out who is right... and who is dead. 
# 
# The line above is from the perennial favorite 1980s movie adaptation of William Goldman's *The Princess Bride*, wherein a mysterious hero sits down to a battle of wits with a villainous Sicilian kidnapper. The setup: two cups positioned between the two, one of which (purportedly) contains a colorless, odorless, lethal poison (viz., iocane powder). After a guess is made as to which cup contains the poison, both drink, and the winner is the one left standing.
# 
# For this machine problem you will write a program that simulates multiple rounds of this battle of wits, allowing the player to repeatedly guess which cup is poisoned. The computer will "place" the poison before the player guesses, and
# will reveal who is right... and who is dead, afterwards.
# 
# At the outset, the computer will always place the poison in cup 2 before letting the player guess, but after enough guesses have been entered the computer will start to place the poison based on the pattern of previous guesses so as to outsmart the player.
# 
# Here's a sample game session (note how the silly player keeps alternating guesses, and that the computer catches on to this fact after a while):
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 1
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 1 times, and I drank the poison 0 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 2
#     Good guess! Ack! I drank the poison!
# 
#     You died 1 times, and I drank the poison 1 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 1
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 2 times, and I drank the poison 1 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 2
#     Good guess! Ack! I drank the poison!
# 
#     You died 2 times, and I drank the poison 2 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 1
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 3 times, and I drank the poison 2 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 2
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 4 times, and I drank the poison 2 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 1
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 5 times, and I drank the poison 2 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 2
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 6 times, and I drank the poison 2 times
# 
#     Where is the iocane powder: my cup (1) or yours (2)? 1
#     Wrong! Ha! Never bet against a Sicilian!
# 
#     You died 7 times, and I drank the poison 2 times
# 
# 
# ## Implementation
# 
# To keep track of the pattern of previous guesses, you will use a dictionary that maps a pattern (of fixed length) to a list of counts for the subsequent guess. 
# 
# For instance, imagine that the computer observes the player continuing to alternate guesses across ten separate attempts, like so: '1', '2', '1', '2', '1', '2', '1', '2', '1', '2'. If we are using a pattern detection length of three, then after the fourth guess we can create an entry in our dictionary that maps the key '121' to the list [0, 1], where the second value (1) in the list indicates that the player guessed '2' following the sequence '1', '2', '1'. After the fifth guess, we create the entry '212' &rarr; [1, 0], and after the sixth guess we update the value for '121' to [0, 2] (since the user guesses '2' again, after the sequence '1', '2', '1').
# 
# Once the player enters a series of guesses that matches a previously seen pattern, the computer should place the poison in the cup that the player is *least likely to guess next*. When the player enters the next guess, the dictionary should be updated to reflect the actual guess.
# 
# This means that if the computer has yet to see a given pattern of guesses, or when the counts are tied, it will have to place the poison "blindly" --- your implementation should simply place the poison furthest away from itself (cup 2). 
# 
# ### `record_guess`
# 
# The first function you are to complete is `record_guess`. It will take the following arguments:
# 
# - a dictionary to update (possibly containing previously recorded pattern &rarr; list mappings)
# - a pattern string
# - a guess -- which is either '1' or '2'.  
# 
# If necessary, the function will create a new entry for the pattern (if one doesn't already exist), then record the updated count for the guess. Since the dictionary is updated in place (i.e., mutated), the function will not return anything. 
# 
# Complete the function below, checking your implementation with the test cases that follow when you're ready. Note that in the future, the bulk of the description for functions we ask you to implement will simply be placed in the functions' docstrings, as below.
# 
# *Hints: the [`int`](https://docs.python.org/3/library/functions.html#int) function can be used to convert strings to integers, and you might find the dictionary's [`setdefault`](https://docs.python.org/3/library/stdtypes.html?highlight=setdefault#dict.setdefault) method useful.*

# In[ ]:


def record_guess(pattern_dict, pattern, guess):
    if pattern in pattern_dict:
        if int(guess) ==1 :
            pattern_dict[pattern][0] += 1
        else:
            pattern_dict[pattern][1] += 1
    else:
        pattern_dict[pattern] = [0,0]
        if int(guess) ==1:
            pattern_dict[pattern][0] += 1
        else:
            pattern_dict[pattern][1] += 1


# In[ ]:


# (5 points)

from unittest import TestCase
tc = TestCase()
d = {}
record_guess(d, '121', '1')
tc.assertDictEqual(d, {'121': [1, 0]})
record_guess(d, '222', '2')
record_guess(d, '121', '1')
tc.assertDictEqual(d, {'121': [2, 0], '222': [0, 1]})
record_guess(d, '122', '2')
record_guess(d, '121', '2')
record_guess(d, '222', '2')
tc.assertDictEqual(d, {'121': [2, 1], '122': [0, 1], '222': [0, 2]})


# ### `next_placement`
# 
# The next function you'll write will take a dictionary of pattern &rarr; counts mappings and a string representing the pattern of most recent guesses, and return the next best location (either '1' or '2') for the poison (i.e., to try and outwit the player). If the pattern hasn't been seen previously or the counts are tied, the function should return '2'.

# In[ ]:


def next_placement(pattern_dict, pattern):
    if pattern in pattern_dict:
        if pattern_dict[pattern][0]<pattern_dict[pattern][1]:
            return '1'
        else:
            return '2'
    else: 
        return '2'


# In[ ]:


# (5 points)

from unittest import TestCase
tc = TestCase()
tc.assertEqual(next_placement({}, '121'), '2')
tc.assertEqual(next_placement({'121': [2, 0]}, '121'), '2')
tc.assertEqual(next_placement({'121': [2, 5]}, '121'), '1')
tc.assertEqual(next_placement({'121': [2, 5]}, '212'), '2')
tc.assertEqual(next_placement({'121': [5, 5]}, '121'), '2')
tc.assertEqual(next_placement({'121': [15, 5]}, '121'), '2')
tc.assertEqual(next_placement({'121': [2, 5],
                               '212': [1, 1]}, '212'), '2')
tc.assertEqual(next_placement({'121': [2, 5],
                               '212': [1, 3]}, '212'), '1')


# ### `play_interactive`
# 
# Now for the fun bit. The function `play_interactive` will take just one argument --- the length of patterns to use as keys in the dictionary --- and will start an interactive game session, reading either '1' or '2' from the player as guesses, using the functions you wrote above and producing output as shown in the sample game session at the beginning of this writeup. If the player types in any other input (besides '1' or '2'), the game should terminate.
# 
# *Hint: the [`input`](https://docs.python.org/3/library/functions.html#input) function can be used to read input from the user as a string.*

# In[ ]:


def play_interactive(pattern_length=4):
    # YOUR CODE HERE
    raise NotImplementedError()


# ### `play_batch`
# 
# Finally, so that we can check your implementation against a lengthier sequence of guesses without having to play an interactive session, implement the `play_batch` function, which will take the `pattern_length` argument as your `play_interactive` function did, but will also take a sequence of guesses. The function will return the total numbers of wins and losses, as determined by the same algorithm as before.

# In[ ]:


def play_batch(guesses, pattern_length=4):
    str = ''
    dict = {}
    c = [0,0]
    for guess in guesses:
        if guess != "1" and guess != "2":
            break
        pred = next_placement(dict,str)
        if guess == pred:
            c[0] += 1
        elif guess != pred:
            c[1] += 1
        if len(str) == pattern_length:
            record_guess(dict,str,guess)
            str = str[1:]
        str += guess
    return tuple(count)


# In[ ]:


# (10 points)

from unittest import TestCase
tc = TestCase()
tc.assertEqual(play_batch(['1', '1', '1', '1', '1', '1'], 3), (0, 6))
tc.assertEqual(play_batch(['1', '2', '1', '2', '1', '2'], 3), (2, 4))
tc.assertEqual(play_batch(['1', '2', '1', '2', '1', '2'], 4), (3, 3))
tc.assertEqual(play_batch(['1', '2'] * 100, 5), (3, 197))
tc.assertEqual(play_batch(['1', '1', '2', '1', '2', '1'] * 100, 2), (398, 202))
tc.assertEqual(play_batch(['1', '1', '2', '1', '2', '1'] * 100, 3), (201, 399))
tc.assertEqual(play_batch(['1', '1', '2', '1', '2', '1'] * 100, 5), (4, 596))
import random
random.seed(0, version=2)
tc.assertEqual(play_batch((random.choice(['1', '2']) for _ in range(10000)), 4), (5047, 4953))


# In[ ]:




