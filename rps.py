'''
Rock Paper Scissors Game
By Abhishek Pagare
'''

import numpy as np
import random

available_choices = ['rock','paper','scissors']

your_choice = input("Choose rock, paper or scissors: ")
comp_choice = np.random.choice(available_choices,1)

if your_choice == 'rock':
    if comp_choice == 'rock':
        print('Computer chose %s, it is a tie!' %comp_choice)
        
    elif comp_choice == 'paper':
        print('Computer chose %s, computer wins!'%comp_choice)
        
    else:
        print('Computer chose %s, you win!'%comp_choice)
        
elif your_choice == 'paper':
    if comp_choice == 'rock':
        print('Computer chose %s, you win!'%comp_choice)
        
    elif comp_choice == 'paper':
        print('Computer chose %s, it is a tie!'%comp_choice)
        
    else:
        print('Computer chose %s, computer wins!'%comp_choice)

else:
    if comp_choice == 'rock':
        print('Computer chose %s, computer wins!'%comp_choice)
        
    elif comp_choice == 'paper':
        print('Computer chose %s, you win!'%comp_choice)
        
    else:
        print('Computer chose %s, it is a tie!'%comp_choice)

