import numpy as np

n = np.random.randint(1,11)

guess = int(input('\nYour guess : '))

number_of_guess = 0

while number_of_guess < 3:
    if guess == n:
        print('\nCorrect guess! The number is ',n)
        break   
    else:
        if n%2 == 0:
            guess = int(input('\nThe number is even. Next Guess :' ))
        else:
            guess = int(input('\nThe number is odd. Next Guess :' ))
    number_of_guess = number_of_guess + 1
    
if number_of_guess > 2:
    print('\nYou have exhausted your choices! \n The number was ',n)    

    