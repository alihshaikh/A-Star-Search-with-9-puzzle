from collections import deque
from copy import deepcopy

#Node class created holding puzzle current state data, h(n) heuristic value, g(n) heuristic value, and array of children Nodes
class Node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hn = 0
        self.gn = 0
        self.children = []


defaultPuzzle = [[1,2,0], [4,5,3], [7,8,6]]

def main():
    print("*****Eight Puzzle Solver*****")
    
    userInput = input("Input 1 to use a default puzzle. Input 2 to create your own puzzle." + '\n')
    puzzle = None

    if int(userInput) == 1:
        puzzle = defaultPuzzle
    elif int(userInput) == 2:
        print('to implement!')
    
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
    #deque library used as our queue https://docs.python.org/3/library/collections.html
    queue = deque()

    root = Node(puzzle)
    queue.append(root)

    while True:
        if len(queue) == 0:
            print ("failure")
            return
        
        node = queue.popleft()
        print(node.puzzle)
        if solved(node.puzzle):
            print ('solved!!!')
            return
        
        operators(node, repeatedStates)
        for i in node.children:
            queue.append(i)

#general operators function testing 4 directional movement of blank space in 8 puzzle
def operators(node, repeatedStates):
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
        temp = board[iLoc+1][jLoc]
        board[iLoc+1][jLoc] = board[iLoc][jLoc]
        board[iLoc][jLoc] = temp
        
        if board not in repeatedStates:
            node.children.append(Node(board))
            repeatedStates.append(board)

    if iLoc > 0:
        board = deepcopy(node.puzzle)
        temp = board[iLoc-1][jLoc]
        board[iLoc-1][jLoc] = board[iLoc][jLoc]
        board[iLoc][jLoc] = temp

        if board not in repeatedStates:
            node.children.append(Node(board))
            repeatedStates.append(board)

    if jLoc < 2:
        board = deepcopy(node.puzzle)
        temp = board[iLoc][jLoc+1]
        board[iLoc][jLoc+1] = board[iLoc][jLoc]
        board[iLoc][jLoc] = temp

        if board not in repeatedStates:
            node.children.append(Node(board))
            repeatedStates.append(board)

    if jLoc > 0:
        board = deepcopy(node.puzzle)
        temp = board[iLoc][jLoc-1]
        board[iLoc][jLoc-1] = board[iLoc][jLoc]
        board[iLoc][jLoc] = temp

        if board not in repeatedStates:
            node.children.append(Node(board))
            repeatedStates.append(board)


    
#used to compare current state puzzle with goal state. returns true if current state = goal state
def solved(puzzle):
    if puzzle == [[1,2,3],[4,5,6],[7,8,0]]:
        return True
    return False


if __name__ == "__main__":
    main()
