matrix = [
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', '*', '*', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', 'e']
]

import dada ##vtori cikul
import treti
import four
import peti


numOfTries=0


def search(x, y):
    global numOfTries
    if matrix[x][y] == 'e':
        return True
    elif matrix[x][y] == '*':
        return False
    elif matrix[x][y] == 'Y':
        return False
    matrix[x][y] = 'Y'
    numOfTries+=1
    if ((x < len(matrix)-1 and search(x+1, y))or (y > 0 and search(x, y-1))or (x > 0 and search(x-1, y))or(y < len(matrix[x])-1 and search(x, y+1))):
        return True
    return False


search(0, 0)
for row in range(len(matrix)):
    print(matrix[row])
print("Cikul 1---Num of tries:",numOfTries)

