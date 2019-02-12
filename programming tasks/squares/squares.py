n = int(input())

if(n < 2 or n > 3):
    exit('Nevaliden n')

size = n**2

check_matrix = []
matrix = []
symbols = []

for i in range(size):
    line = input().split()
    arr = []
    for x in range(len(line)):
        arr.append(line[x])

    matrix.append(line)
    check_matrix.append(arr)

for i in range(size):
    for j in range(size):
      if matrix[i][j] not in symbols:
          if matrix[i][j] != '0':
            symbols.append(matrix[i][j])

def isValid(x, y, s):
    correct = True
    x1 = n*(x//n)
    x2 = n + n*(x//n)
    x3 = n*(y//n)
    x4 = n + n*(y//n)

    for k in range(size):
        if matrix[x][k] == s or matrix[k][y]==s: # test if symbol in row
          correct = False
          
    for k in range(x1, x2): # test if symbol in square
      for l in range(x3, x4):
        if matrix[k][l] == s:
          correct = False
          
    return correct

def next(x1, x2):
    if x1 == size-1:
        return (0, x2+1)
    else:
        return (x1+1, x2)

def Checker(x, y):
    nextX = next(x, y)
    if(matrix[x][y] == '0'):
        for s in symbols:
            if isValid(x, y, s):
                matrix[x][y] = s
                if isSolved():
                    print('Result:')
                    for i in range(size):
                        for j in range(size):
                            if matrix[i][j] == check_matrix[i][j]:
                                print('' + matrix[i][j] + '', end="  ")
                            else:
                                print('' + matrix[i][j] + '', end="  ")
                        print('\n')
                else:
                    Checker(nextX[0], nextX[1])
        matrix[x][y] = '0'
    else:
        if x != size-1 or y != size-1:
            Checker(nextX[0], nextX[1])

def isSolved():
    solved = True
    for x in range(size):
        for y in range(size):
            if matrix[x][y] == '0':
                solved = False
    return solved

Checker(0, 0)
