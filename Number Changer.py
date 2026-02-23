# Python Project 1  :Random Number Generator
# Author            :Maze Elva 
# Date              :2026-02-15
# This program will ask for a number and a number of steps, and 
# each step will either increase the number by 2 or decrease it by 1.

import math, random

def gen(number):
    select = random.randint(0, 1)

    if select == 0:
        number += 2
    elif select == 1:
        number -= 1

    return(number)

def get_number():
    valid = False
    while not valid:
        print('')
        try:
            number = int(input('Please select an integer between 1 and 10 \n:'))
            if not 0 < number < 11:
                print('-Error- Value must be between 1 and 10')
            else:
                valid = True

        except(ValueError):
            print('-Error- Value must be an integer')


    valid = False
    while not valid:
        print('')
        try:
            iterate_count = int(input('Please enter an integer for the amount of times the number will be changed. \n(Dont make it too high.) \n:'))
            if not iterate_count > 0:
                print('-Error- You cant have negative iterations')
            else:
                valid = True

        except(ValueError):
            print('-Error- Value must be an integer')

    return(number, iterate_count)

def iterate(number, iterate_count):
    for i in range(iterate_count):
        number = gen(number)
        print(f'Iteration: {i+1} \n\tNumber is: {number}')

number, iterate_count = get_number()
iterate(number, iterate_count)

end = False
while not end:
    reset = str.lower(input('\nDo you want to go again?\n:'))
    if reset == 'y' or reset == 'yes':
        number, iterate_count = get_number()
        iterate(number, iterate_count)
    elif reset == 'n' or reset == 'no':
        end = True

    else:
        print('Something went wrong, please enter either y, n, yes, or no')
