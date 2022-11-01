from copy import deepcopy

#Node class created holding puzzle current state data, h(n) heuristic value, depth value, and array of children Nodes
class Node:
    def __init__(self, puzzle, hn, depth):
        self.puzzle = puzzle
        self.hn = hn
        self.depth = depth
        self.children = []


defaultPuzzle = [[8,7,1], [6,0,2], [5,4,3]]


def main():
    print("*****Eight Puzzle Solver*****")
    
    userInput = input("Input 1 to use a default puzzle. Input 2 to create your own puzzle." + '\n')
    puzzle = None

    if int(userInput) == 1:
        puzzle = defaultPuzzle
    elif int(userInput) == 2:
        print("Create your own puzzle using a zero to represent the blank tile. " + "Please only enter valid 8-puzzles. Sepa2rate each value with a space and hit ENTER after inputting each row" + '\n')

        #input() was faulty -- used raw_input() to fix issue. https://stackoverflow.com/questions/17611391/python-invalid-syntax-on-line-1-file-string 
        rowOne = raw_input('Enter the first row: ')
        rowTwo = raw_input("Enter the second row: ")
        rowThree = raw_input("Enter the third row: ")
        
        rowOne = rowOne.split()
        rowTwo = rowTwo.split()
        rowThree = rowThree.split()

        for i in range(0,3):
            rowOne[i] = int(rowOne[i])
            rowTwo[i] = int(rowTwo[i])
            rowThree[i] = int(rowThree[i])
        
        puzzle = [rowOne, rowTwo, rowThree]
        
    print('\n') 
    print("*****Algorithm Selector*****")
    
    algoInput = input("Type the number for the corresponding algorthm option: Uniform Cost Search: 1, Misplaced Tile Heuristic: 2, Manhattan Distance Heuristic: 3" + '\n')

    #Given input, pass in 1,2, or 3, indicating what kind of "heuristic" to use in our search algorith,
    if int(algoInput) == 1:
        general_search(puzzle, 1)
    elif int(algoInput) == 2:
        general_search(puzzle, 2)
    elif int(algoInput) == 3:
        general_search(puzzle,3)

#CS170 "General" Search Algorithm which is tailored based on the input "queueing_function"
def general_search(puzzle, queueing_function):
    #array to store our states that have been seen. used to determine if current expansion node state is a duplicate.
    repeatedStates = []
    largestSizeOfQueue = -1
    nodesExpanded = 0
    queue = []

    if queueing_function == 3:
        root = Node(puzzle, manhattan(puzzle), 0)
    if queueing_function == 2:
        root = Node(puzzle, misplaced(puzzle), 0)
    else:
        root = Node(puzzle, 1, 0)
    
    queue.append(root)

    while True:
            if len(queue) == 0:
                print ("failure")
                return
            
            largestSizeOfQueue = max(largestSizeOfQueue, len(queue))
            if queueing_function == 2 or queueing_function == 3:
                #use lambda function to sort queue (array) with respect to object attributes https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
                queue = sorted(queue, key=lambda x: (x.hn + x.depth))
            
            node = queue[0]
            queue.pop(0)
            
            print("The best state to expand with g(n) = " + str(node.depth) + " and h(n) = " + str(node.hn) + " is: ")
            print(node.puzzle)

            if solved(node.puzzle):
                print('\n')
                print ('Solved!!! Goal state found.')
                print('Solution depth was ' + str(node.depth))
                print('Number of nodes expanded was ' + str(nodesExpanded))
                print('Max queue size was ' + str(largestSizeOfQueue))
                return
            
            operators(node, repeatedStates, queueing_function, nodesExpanded)

            for i in node.children:
                queue.append(i)
            nodesExpanded +=1

#general operators function testing 4 directional movement of blank space in 8 puzzle
def operators(node, repeatedStates, queueing_function, nodesExpanded):
    iLoc = 0
    jLoc = 0

    #find index [i,j] of 0 in the puzzle
    for i in range(3):
        for j in range(3):
            if node.puzzle[i][j] == 0:
                iLoc = i
                jLoc = j

    if iLoc < 2:
        #deepcopy is used to ensure our parent board is not changed for all operator permutations
        #https://docs.python.org/3/library/copy.html
        board = deepcopy(node.puzzle)
        upOperator(board,iLoc,jLoc)
         
        if board not in repeatedStates:
            if queueing_function == 1:
                node.children.append(Node(board, 1, node.depth+1))
            elif queueing_function == 2:
                node.children.append(Node(board, misplaced(board), node.depth+1))
            elif queueing_function == 3:
                node.children.append(Node(board, manhattan(board), node.depth+1))
            repeatedStates.append(board)
            

    if iLoc > 0:
        board = deepcopy(node.puzzle)
        downOperator(board, iLoc, jLoc)

        if board not in repeatedStates:
            if queueing_function == 1:
                node.children.append(Node(board, 1, node.depth+1))
            elif queueing_function == 2:
                node.children.append(Node(board, misplaced(board), node.depth+1))
            elif queueing_function == 3:
                node.children.append(Node(board, manhattan(board), node.depth+1))
            repeatedStates.append(board)

    if jLoc < 2:
        board = deepcopy(node.puzzle)
        rightOperator(board, iLoc, jLoc)

        if board not in repeatedStates:
            if queueing_function == 1:
                node.children.append(Node(board, 1, node.depth+1))
            elif queueing_function == 2:
                node.children.append(Node(board, misplaced(board), node.depth+1))
            elif queueing_function == 3:
                node.children.append(Node(board, manhattan(board), node.depth+1))
            repeatedStates.append(board)
            
    if jLoc > 0:
        board = deepcopy(node.puzzle)
        leftOperator(board, iLoc, jLoc)

        if board not in repeatedStates:
            if queueing_function == 1:
                node.children.append(Node(board, 1, node.depth+1))
            elif queueing_function == 2:
                node.children.append(Node(board, misplaced(board), node.depth+1))
            elif queueing_function == 3:
                node.children.append(Node(board, manhattan(board), node.depth+1))
            repeatedStates.append(board)

#moves blank space in 8 puzzle in upwards direction
def upOperator(board, iLoc, jLoc):
    temp = board[iLoc+1][jLoc]
    board[iLoc+1][jLoc] = board[iLoc][jLoc]
    board[iLoc][jLoc] = temp

#moves blank space in 8 puzzle in downwards direction    
def downOperator(board, iLoc, jLoc):
    temp = board[iLoc-1][jLoc]
    board[iLoc-1][jLoc] = board[iLoc][jLoc]
    board[iLoc][jLoc] = temp

#moves blank space in 8 puzzle in right direction
def rightOperator(board, iLoc, jLoc):
    temp = board[iLoc][jLoc+1]
    board[iLoc][jLoc+1] = board[iLoc][jLoc]
    board[iLoc][jLoc] = temp

#moves blank space in 8 puzzle in left direction
def leftOperator(board, iLoc, jLoc):
    temp = board[iLoc][jLoc-1]
    board[iLoc][jLoc-1] = board[iLoc][jLoc]
    board[iLoc][jLoc] = temp

#returns misplaced tile heuristic
def misplaced(board):
    numMisplaced = 0
    comparisonBoard = [[1,2,3],[4,5,6],[7,8,0]]

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                continue
            if board[i][j] != comparisonBoard[i][j]:
                numMisplaced +=1
    return numMisplaced

#returns manhattan distance heuristic
def manhattan(board):
    comparisonBoard = [[1,2,3],[4,5,6],[7,8,0]]
    total = 0
    currentRow = 0
    currentCol = 0
    realRow = 0
    realCol = 0

    realLocation = {1: [0,0], 2: [0,1], 3: [0,2], 4: [1,0], 5: [1,1], 6: [1,2], 7: [2,0], 8: [2,1]}

    for i in range(3):
        for j in range(3):
            if board[i][j] != comparisonBoard[i][j] and board[i][j] != 0:
                realRow = realLocation[board[i][j]][0]
                realCol = realLocation[board[i][j]][1]
                currentRow = i
                currentCol = j
            total += abs(realRow-currentRow) + abs(realCol - currentCol)
    return total

#used to compare current state puzzle with goal state. returns true if current state = goal state
def solved(puzzle):
    if puzzle == [[1,2,3],[4,5,6],[7,8,0]]:
        return True
    return False

if __name__ == "__main__":
    main()

