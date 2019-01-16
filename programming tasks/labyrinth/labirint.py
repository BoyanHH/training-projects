#*->stena
#''->moje da se mine
#e->izhod
#Trugva se ot matrix[0][0]


matrix = [
[' ', ' ', ' ', '*', ' ', '*', ' '],
['*', '*', ' ', '*', ' ', '*', ' '],
[' ', ' ', ' ', '*', ' ', ' ', ' '],
[' ', ' ', '*', '*', ' ', '*', ' '],
['*', ' ', '*', '*', '*', '*', ' '],
[' ', 'e', ' ', ' ', ' ', ' ', ' ']

]
##matrix = [
##[' ', '*', ' ', ' ', ' ', '*', ' '],
##[' ', '*', ' ', '*', ' ', '*', ' '],
##[' ', '*', ' ', ' ', ' ', ' ', ' '],
##[' ', '*', '*', '*', ' ', '*', '*'],
##[' ', '*', ' ', '*', ' ', '*', ' '],
##[' ', '*', ' ', ' ', ' ', '*', ' '],
##[' ', ' ', '*', '*', '*', '*', ' '],
##[' ', ' ', '*', '*', ' ', '*', '*'],
##[' ', '*', ' ', '*', ' ', '*', ' '],
##[' ', ' ', ' ', ' ', ' ', ' ', ' '],
##['*', '*', '*', '*', '*', '*', ' '],
##[' ', ' ', ' ', ' ', ' ', ' ', 'e']
##]

rows =  len(matrix) -1
cols =  len(matrix[0]) -1

red=0
kolona=0

while(True):
    try:
        print(cols)
        print(rows)
        print("-------------------current matrix---------------")
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        for row in matrix]))                    
        print("------------------------------------------------")
        if(kolona==cols):
            while(True):
                if(matrix[red+1][kolona]==' '):
        #uspeshno
                    red+=1
                    matrix[red][kolona]='Y'    
                elif(matrix[red+1][kolona]=='*'):
            #ako i nadolu i nadqsno sme do stena, TODO
                    print("todo")
                
                if(matrix[red+1][kolona]=='e'):
                    matrix[red+1][kolona]='Y'
                    print("-------------------current matrix---------------")
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                    for row in matrix]))                    
                    print("------------------------------------------------")
                    exit("GOT OUT")
                if(matrix[red][kolona]=='e'):
                    exit("GOT OUT")
        if(red!=4):
            if(matrix[red+1][kolona]== ' '):
                 red+=1
                 matrix[red][kolona]='O'
        if(matrix[red][kolona+1]==' '):
        #ako sledvashtata vdqsno sushto e '' se premestvame
                 print("kolona +1")
                 kolona+=1
                 matrix[red][kolona]='Y'                
        elif(kolona<=cols and matrix[red][kolona+1]=='*'):
        #ako sledvashtoto e *, to e stena i ne mojem.
        #probvame nadolu.
            if(matrix[red+1][kolona]==' '):
        #uspeshno
                red+=1
                matrix[red][kolona]='Y'    
            elif(matrix[red+1][kolona]=='*'):
        #ako i nadolu i nadqsno sme do stena, TODO
                check=True
                while kolona>0:
                ########################################
                    print(cols)
                    print(rows)
                    print("-------------------current matrix---------------")
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                    for row in matrix]))                    
                    print("------------------------------------------------")
                    if(kolona==cols):
                        if(matrix[red+1][kolona]==' '):
                #uspeshno
                            red+=1
                            matrix[red][kolona]='Z'
                    try:
                        if(matrix[red+1][kolona]=='*'):
                    #ako i nadolu i nadqsno sme do stena, TODO
                            print("todo")
                    except IndexError:
                        print("q")
                    try:
                        if(matrix[red+1][kolona]=='e'):
                            matrix[red+1][kolona]='Z'
                            print("-------------------current matrix---------------")
                            print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                            for row in matrix]))                    
                            print("------------------------------------------------")
                            exit("GOT OUT")
                        if(matrix[red][kolona]=='e'):
                            exit("GOT OUT")
                      #  if(rows<10):
                        if(matrix[red+1][kolona]== ' '):
                             red+=1
                             matrix[red][kolona]='O'
                    except IndexError:
                        print("gg")
                    try:
                        if(matrix[red][kolona+1]==' '):
                        #ako sledvashtata vdqsno sushto e '' se premestvame
                                 print("kolona +1")
                                 kolona+=1
                                 matrix[red][kolona]='Z'
                        elif(kolona<=cols and matrix[red][kolona+1]=='*'):
                    #ako sledvashtoto e *, to e stena i ne mojem.
                    #probvame nadolu.
                            if(matrix[red-1][kolona]==' '):
                    #uspeshno
                                red-=1
                                matrix[red][kolona]='Z'    
                            elif(matrix[red-1][kolona]=='*'):
                                red-=1
                                matrix[red][kolona]='Z'                            
                        if(matrix[red+1][kolona]=='e'):
                            exit("GOT OUT")
                        if(matrix[red][kolona]=='e'):
                            exit("GOT OUT")    
                        if(matrix[red][kolona-1]==' '):
                                print("kolona -1")
                                kolona-=1
                                matrix[red][kolona]='C'       
                    except IndexError:
                        print("a")
                               
                ################################
                print("todo")
        if(matrix[red][kolona]=='e'):
            exit("GOT OUT")
        #except IndexError:
          #  print(red)
    except IndexError:
        print("fff")


