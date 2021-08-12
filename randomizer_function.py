'''
Coded by Abhishek Pagare
This code gives you random question numbers to solve from an exercise.
You need to enter total number of codes in the exercise, the code will give 
    you 1/3rd of the total number of the questions in the exercise.
    
'''


import numpy as np
import math
import pandas as pd

class randomizer:
    def __init__(self,number_of_questions):
        self.number_of_questions = number_of_questions
        global to_solve                #to use this variable outside the class
        to_solve = number_of_questions/2.5
        to_solve = math.ceil(to_solve)           #rounding off to next integer
        print("\n You have to solve %d questions from this exercise."%to_solve)
        global randomized_array
        randomized_array = list(np.random.choice(np.arange(1,number_of_questions+1),to_solve,replace=False)) #gives a list of non-repetitive random numbers between total number of questions 
        randomized_array.sort()            #sorting the list in ascending order
        print("\nRandom question numbers are: ",randomized_array)
        

number_of_questions = int(input("\nEnter the number of questions in this exercise: "))

chapter = randomizer(number_of_questions) #creating an instance of the class

approval_answers = ['yes','Y','Yes','y','YES']

approval = str(input("\nAre you fine with the questions? :"))

while approval not in approval_answers:  #This loop will ask you if random questions are okay or not. If they are not, the code will generate new random numbers.
    print("\nThe randomizer will run again.")
    chapter = randomizer(number_of_questions)
    approval = str(input("\nAre you fine with the questions? : "))

'''
next lines of code are just to register your answers in the answers array.
this array will be printed after you complete solving exercise, for you to 
    check your answers from solutions

'''
answers = [] 
for i in range(0,len(randomized_array)):
    answers.insert(i,input("\n Enter the answer of question number %d: "%randomized_array[i]))

change = str(input('\nDo you want to change any answers? :'))

change_answers = ['yes','y','YES','Y','Yes']

change_number = 0

while change in change_answers:
    change_number = int(input('\nEnter the question to which you have to change the answer: '))
    change_answer = str(input('\nEnter your answer: '))
    index = randomized_array.index(change_number)
    answers[index] = change_answer
    change = str(input('\nDo you want to change any answers? :'))
    

a = list(zip(randomized_array,answers))

Table = pd.DataFrame(a,columns=['Question no.','Answers'])

print("\nYour answers are : \n")
print(Table)

