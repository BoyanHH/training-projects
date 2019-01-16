matrix = [
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', '*', '*', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', 'e']
]
numOfTries=0


def search2(x, y):
    global numOfTries
    if matrix[x][y] == 'e':
        return True
    elif matrix[x][y] == '*':
        return False
    elif matrix[x][y] == 'Y':
        return False
    matrix[x][y] = 'Y'
    numOfTries+=1
    if ((x < len(matrix)-1 and search2(x+1, y))or(y < len(matrix[x])-1 and search2(x, y+1)) or (x > 0 and search2(x-1, y)) or (y > 0 and search2(x, y-1))):
        return True
    return False


search2(0, 0)
for row in range(len(matrix)):
    print(matrix[row])
print("Cikul 3---Num of tries:",numOfTries)
