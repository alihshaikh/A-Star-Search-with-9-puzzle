import heapq
from collections import deque
from re import L
from copy import copy, deepcopy


class TreeNode:
    def __init__(self, boardData, i, j):
        self.children = []
        self.data = boardData
        self.i = i
        self.j = j

trivial = [[1,2,3], [4,5,6], [7,8,0]]

veryEasy = [[1,2,3], [4,5,6], [7,0,8]]

easy = [[1,2,0], [4,5,3], [7,8,6]]

doable = [[0, 1, 2],
[4, 5, 3],
[7, 8, 6]]
oh_boy = [[8, 7, 1],
[6, 0, 2],
[5, 4, 3]]

eightGoalState = [[1,2,3],[4,5,6],[7,8,0]]

def main():
    # puzzleMode = input('8-puzzle solver. Please choose one of the following options:' + '\n')

    
    uniformCostSearch(doable)


def uniformCostSearch(board):
    startingI = None
    startingJ = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                startingI = i
                startingJ = j
                

    startNode = TreeNode(board, startingI, startingJ)
    repeatedStates = {} # dictionary (hashmap) used to avoid exploring redundant (similar) states. O(1) lookup O(n) space.
    queue = deque()
    queue.append(startNode)
#    >>> tuple(map(tuple, arr))
    repeatedStates[tuple(map(tuple,startNode.data))] = "this is the root board"
    numCount = 1
    while queue:
        cur = queue.popleft()
        if solved(cur.data):
            print('solved')
            print('total nodes in search space: ')
            print(numCount)
            break
        else:
            numCount +=1
        if cur.i < len(cur.data)-1:
            copyBoard = deepcopy(cur.data)
            cur.children.append(downOperator(copyBoard, cur.i, cur.j))
            # queue.append(downOperator(cur.data, i, j))

        if cur.i > 0:
            copyBoard = deepcopy(cur.data)
            cur.children.append(upOperator(copyBoard, cur.i, cur.j)) 
            # queue.append(upOperator(cur.data, i, j))

        if cur.j < len(cur.data[cur.i])-1:
            copyBoard = deepcopy(cur.data)
            cur.children.append(rightOperator(copyBoard, cur.i, cur.j))
            # queue.append(rightOperator(cur.data, i, j))

        if cur.j > 0:
            copyBoard = deepcopy(cur.data)
            cur.children.append(leftOperator(copyBoard, cur.i, cur.j))
            # queue.append(leftOperator(cur.data, i, j))

        for instance in cur.children:
            queue.append(instance)



# [1,2,3]
# [4,5,6]
# [7,0,8]
#curI = 2
#curJ = 1
def downOperator(board, i, j):
    temp = board[i+1][j]
    board[i+1][j] = board[i][j]
    board[i][j] = temp
    return TreeNode(board, i+1 ,j)

def upOperator(board,i,j):
    temp = board[i-1][j]
    board[i-1][j] = board[i][j]
    board[i][j] = temp
    return TreeNode(board, i-1 ,j)

def rightOperator(board,i,j):
    temp = board[i][j+1]
    board[i][j+1] = board[i][j]
    board[i][j] = temp
    return TreeNode(board, i, j+1)

def leftOperator(board,i,j):
    temp = board[i][j-1]
    board[i][j-1] = board[i][j]
    board[i][j-1] = temp
    return TreeNode(board, i, j-1)


def solved(board):
    if board == eightGoalState:
        return True
    return False

main()