import time
import pyautogui as pp
from z3 import Solver, Sum, Int, If, And, Or, sat
import pydirectinput as pdi

def createGraph(n, m):
    matrix = [[0 for j in range(m)] for i in range(n)]
    return matrix

def locateEm(n,m):
    matrix = createGraph(n,m)
    matrix_of_loc=createGraph(n,m)

    dict_of_next = {5: (544, 786) , 6:(540,840) , 7:(542,889) ,8:(540,891),
                    9:(542,891),10:(542,890),11:(542,890),12:(545,892),
                    13:(545,892),14:(543,893)}

    dict_of_coords = {5: (275,300,100), 6: (230,250,96),7: (182,205,99),8: (176,194,85),
                      9: (166,190,78),10: (166,184,71),11: (161,182,63),12: (158,181,59),
                      13: (153,178,54) ,  14: (151,177,50)}

    x,y,k = dict_of_coords[n]
    # Blue = 1, Red = 2, Orange = 3, Yellow = 4, Green = 5
    dict_of_colours = {(0, 0, 255): 1, (255, 0, 0): 2, (0, 128, 0): 3, (238, 238, 0): 4,
                       (255, 127, 0): 5,(255, 0, 255): 6,(128, 0, 128): 7, (0, 255, 255): 8,
                       (0, 128, 128): 9, (0, 0, 139): 10,(166, 166, 166): 11,(189, 183, 107): 12,
                       (0, 255, 0): 13, (165, 42, 42): 14, (255, 255, 255): 15,(128, 128, 128): 16}

    for i in range(n):
        x = dict_of_coords[n][0]
        for j in range(m):
            coloVal= pp.pixel(x,y)
            if coloVal in dict_of_colours.keys():
                matrix[i][j] = dict_of_colours[coloVal]
            matrix_of_loc[i][j] = (x,y)
            x+=k
        y+=k

    return matrix,matrix_of_loc,dict_of_next
def solveEm(board,n):
    M = n
    N = n
    B = [[Int(f'B_{i}_{j}') for j in range(N)] for i in range(M)]

    s = Solver()

    s.add(([If(board[i][j] != 0, B[i][j] == board[i][j], And(B[i][j] >= 1, B[i][j] < 90))
            for j in range(N) for i in range(M)]))

    for i in range(M):
        for j in range(N):
            same_neighs_ij = Sum([If(B[i][j] == B[k][l], 1, 0)
                                  for k in range(M) for l in range(N) if
                                  abs(k - i) + abs(l - j) == 1])  # Manhattan distance
            if board[i][j] != 0:
                s.add(same_neighs_ij == 1)
            else:
                s.add(Or(same_neighs_ij == 2, B[i][j] == 0))

    if s.check() == sat:
        m = s.model()
        S = [[m[B[i][j]].as_long() for j in range(N)] for i in range(M)]
        return S

def displayMatrix(finalM):
    for row in finalM:
        print(row)

def JustMoveOver(locations):
    for i in locations:
        for j in i:
            x,y=j
            pp.moveTo(x,y)
            time.sleep(0.1)
def findSrcandDest(ogmatrix):
    coordinates = {}
    for i in range(len(ogmatrix)):
        for j in range(len(ogmatrix[0])):
            cur = ogmatrix[i][j]
            if cur != 0:
                if cur not in coordinates:
                    coordinates[cur] = {'src': (i, j), 'dest': None, 'path': []}
                else:
                    coordinates[cur]['dest'] = (i, j)
    return coordinates

def is_valid_move(matrix, visited, current_position, next_position,no):
    i, j = next_position
    return 0 <= i < len(matrix) and 0 <= j < len(matrix[0]) and not visited[i][j] and matrix[i][j] == no

def dfs(matrix, visited, current_position, target_position, path, all_paths,no):
    i, j = current_position
    visited[i][j] = True
    path.append(current_position)

    if current_position == target_position:
        all_paths.append(path.copy())
    else:
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_position = (i + di, j + dj)
            if is_valid_move(matrix, visited, current_position, next_position,no):
                dfs(matrix, visited, next_position, target_position, path, all_paths,no)

    path.pop()
    visited[i][j] = False
def extract_number(matrix, target_number):
    return [[cell if cell == target_number else 0 for cell in row] for row in matrix]

def dragemm(pathie,loc_matrix):
    print(pathie)
    coords_list = pathie
    initial_x, initial_y = loc_matrix[coords_list[0][0]][coords_list[0][1]]
    pdi.moveTo(initial_x, initial_y)  # Move to the initial position
    pdi.mouseDown()  # Simulate mouse down

    for x, y in coords_list[1:]:
        target_x, target_y = loc_matrix[x][y]
        pdi.moveTo(target_x, target_y)  # Move to the next position
        time.sleep(.1) #change this to drage faster

    last_x, last_y = loc_matrix[coords_list[-1][0]][coords_list[-1][1]]
    pdi.moveTo(last_x, last_y)  # Move to the last position
    pdi.mouseUp()  # Simulate mouse up

def finalPath(no,matrix,coord,positionsonmap):

    num = sum(row.count(no) for row in matrix)
    M = len(matrix)
    N = len(matrix[0])

    visited = [[False for _ in range(N)] for _ in range(M)]
    path = []
    all_paths = []

    start_position = coord[no]['src']
    target_position = coord[no]['dest']
    print(f'No : {no} src = {start_position} dest = {target_position}')

    dfs(matrix, visited, start_position, target_position, path, all_paths,no)

    if all_paths:
        print(f"All paths covering all {no}'s theer are {num}:")
        for idx, path in enumerate(all_paths, start=1):
            print(f"Path {idx}: {path} \n Len:{len(path)}")
            dragemm(path,positionsonmap)
    else:
        print("No valid paths found.")
def finalPathsOfAllNumbs(solvedMat,src_dest,locationz):
    for number in set(cell for row in solvedMat for cell in row):
        extracted_matrix = extract_number(solvedMat, number)
        finalPath(number,extracted_matrix,src_dest,locationz)
        print()

#-----MAINNN-------

no_of_puzzles = 1

for i in range(no_of_puzzles):

    time.sleep(2)

    for x in range(5, 15):
        # put your dir path here
        image_path = fr'boardsize\{x}.png'
        if pp.locateOnScreen(image_path, confidence=0.85) != None:
            ans = x
            break

    ogmat,locMat , nextDict= locateEm(ans,ans)
    src_dest = findSrcandDest(ogmat)
    print('Detected Matrix: ')
    displayMatrix(ogmat)

    #JustMoveOver(locMat)
    solvedMat = solveEm(ogmat,ans)
    print('Solved Matrix: ')
    displayMatrix(solvedMat)

    print('loc Matrix: ')
    displayMatrix(locMat)

    finalPathsOfAllNumbs(solvedMat,src_dest,locMat)

    x,y = nextDict[ans]

    # to click the next button
    pdi.click(x,y)
    pdi.click(x, y)

