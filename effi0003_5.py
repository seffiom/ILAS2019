#!/usr/bin/env python
# coding: utf-8

# In[16]:


#Samuel Effiom 113387836
import random
def randintlist(minimum,maximum,length):
    li = [] #creates empty list
    while(len(li)< length): #while condition till the list becomes the length provided
        ran = random.randint(minimum,maximum) #generates random number between min & max 
        if ran in li:
            continue #means skip
        else:
            li.append(ran)
    return li

print('Welcome to my Guessing Game.')
print('Difficulty can be either easy, medium, or hard.')

difficulty = input('Which difficulty level do you want to play?')
while difficulty not in ('easy','medium','hard'): #prompt user to enter easy, medium or hard only 
    difficulty = input('Which difficulty level do you want to play?')
print(difficulty)

if difficulty == 'easy':
    result = randintlist(1,10,5) #generating random list with length = 5 
elif difficulty == 'medium':
    result = randintlist(1,10,3) #generating random list with length = 3
elif difficulty == 'hard':
    result = randintlist(1,10,1) #generating random list with length = 1
    
guess = int(input('Guess a number between 1 and 10:'))
while guess > 10 or guess < 1: #prompt user to enter values between 1 and 10 only 
    guess = int(input('Guess a number between 1 and 10:'))
#checks if the guessed number is or not in the generated list from the randintlist function 
if guess not in result:
    print('You lost')
else:
    print('You won')

print('Thanks for playing my Guessing game')

