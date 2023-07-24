''' Jonathan Koch
Program Implements A* Pathfinding Algorithm to solve the 8-Tile Game.
'''

from heap_queue import HeapQueue
import math
import os
import numpy as np
from enum import Enum

class Actions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Node:
    def __init__(self, id=0):
        self.id = id
        self.neighbors = {
            Actions.UP: None,
            Actions.DOWN: None,
            Actions.LEFT: None,
            Actions.RIGHT: None
        }
    def reset_neighbors(self):
        self.neighbors = {
            Actions.UP: None,
            Actions.DOWN: None,
            Actions.LEFT: None,
            Actions.RIGHT: None
        }
    
    def copy(self):
        return Node(self.id)
    
    def __eq__(self, other):
       return id(self) == id(other)
   
    def __str__(self):
        return f"Node: {self.id}"
    def __repr__(self):
        return self.__str__()

    
    
class Path:
    END_CONFIG = np.array([[1,2,3],[8,0,4],[7,6,5],])
    def __init__(self, seen_configs, board):
        self._board = board
        self._current_config = self._board.get_configuration()
        if seen_configs is None:
            self.seen_configs = []
        else:
            self.seen_configs = seen_configs
            
        if not self.is_in_path(self._current_config):
            self.seen_configs.append(self._current_config)   
            
        self.actions_path = []
        self._cost = 0
        self.heuristic = math.inf

    def current_state(self):
        return self._current_config
    
    def get_actions(self):
        return self._board.get_actions()
    

    def is_in_path(self, config):
        # Go Backwards to Speed up finding recently seen configs
        for c in self.seen_configs[-len(self.seen_configs)::]:
            if np.array_equal(c, config):
                return True
        return False
    
    def _get_index_of(self, id, config=None):
        if config is None:
            for i in range(len(self._current_config)):
                for j in range(len(self._current_config[i])):
                    if self._current_config[i][j] == id:
                        return i, j
        else:
            for i in range(len(self._current_config)):
                for j in range(len(self._current_config[i])):
                    if config[i][j] == id:
                        return i, j
            
    #Distance from Correct Position Manhattan Distance
    def heuristic_1(self):
        running_h = 0
        for i in range(1, 9):
            row, col = self._get_index_of(i)
            desired_row, desired_col = self._get_index_of(i, self.END_CONFIG)
            running_h += abs(row - desired_row) + abs(col - desired_col)
        return running_h
    
    #Euclidian Distance
    def heuristic_2(self):
        running_h = 0
        for i in range(1, 9):
            row, col = self._get_index_of(i)
            desired_row, desired_col = ((i-1)//3), ((i-1)%3)
            distance = np.sqrt((row - desired_row)**2 + (col-desired_col)**2)
            if distance > 0: 
                running_h+=1
                continue
                
            running_h += distance
        return running_h
    
    def _update_heuristic(self):
        if len(self.actions_path) == 0:
            self.heuristic = math.inf
        else:
           self.heuristic = self.heuristic_1()
           
    def cost(self):
        self._update_heuristic()
        return self.heuristic + self._cost

    def copy(self):
        p = Path( None, self._board.copy())
        p._current_config = np.copy(self._current_config)
        for action in self.actions_path:
            p.actions_path.append(action)
        p._cost = self._cost
        for config in self.seen_configs:
            if not p.is_in_path(config):
                p.seen_configs.append(config)
        p._update_heuristic()
        
        return p
        
    def step(self, action):
        n_board, cost = self._board.step(action)
        n_path = self.copy()
        n_path._board = n_board
        n_path.actions_path.append(action)
        n_path._cost += cost
        n_path._current_config = n_path._board.get_configuration()
        n_path.seen_configs.append(n_path._current_config)
        n_path._update_heuristic()
        return n_path

    def __lt__(self, other):
            return self.cost() < other.cost()
    def __gt__(self, other):
            return self.cost() > other.cost()
    def __eq__(self, other):
            return self.cost() == other.cost()
    def __str__(self):
        return f"Path: {self.actions_path}\Cost: {self._cost}, Heuristic: {self.heuristic_1()}"

    def found_path(self):
        return self.is_in_path(self.END_CONFIG)
   

class Board:
    def _init_board(self):
        rows = []
        for i in range(3):
            cols = []
            for j in range(3):
                cols.append(Node())
            rows.append(cols)
        return np.array(rows)
    def __init__(self):
        self.nodes = []
        self.board = self._init_board()
        
    def _get_state_node(self):
        for node in self.nodes:
            if node.id == 0:
                return node
    @classmethod
    def get_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def copy(self):
        new_board = Board()
        idxI, idxJ = self.board.shape
        for i in range(idxI):
            for j in range(idxJ):
                new_board.board[i][j] = self.board[i][j].copy()
        Board.Initialize(new_board)
        return new_board
    
    def _get_index_of(self, id):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].id == id:
                    return i, j
    
    @staticmethod
    def Initialize(board:'Board'):
        board.nodes = []
        for idxI in range(3):
            for idxJ in range(3):
                board.nodes.append(board.board[idxI][idxJ])
                board.board[idxI][idxJ].reset_neighbors()
                if idxI > 0:
                    board.board[idxI][idxJ].neighbors[Actions.UP] = board.board[idxI-1][idxJ]
                if idxI < 2:
                    board.board[idxI][idxJ].neighbors[Actions.DOWN] = board.board[idxI+1][idxJ]
                if idxJ > 0:
                        board.board[idxI][idxJ].neighbors[Actions.LEFT] = board.board[idxI][idxJ-1]
                if idxJ < 2:
                    board.board[idxI][idxJ].neighbors[Actions.RIGHT] = board.board[idxI][idxJ+1]
    
    def get_actions(self):
        idx = self._get_index_of(0);
        actions = []
        for action, node in self.board[idx[0], idx[1]].neighbors.items():
            if node is not None:
                actions.append(action)
        return actions
     
    def step(self, action):
        new_board = self.copy()
        idx = new_board._get_index_of(0)
        zero_node = new_board.board[idx[0], idx[1]]
        update_node = zero_node.neighbors[action]
        if update_node is not None:
            zero_node.id = update_node.id
            update_node.id = 0
        else:
            print("ERROR: Null Node")

        return new_board, zero_node.id
       
    def get_configuration(self):
        rows = []
        for i in range(3):
            col = []
            for j in range(3):
                col.append(self.board[i][j].id)
            rows.append(col)
        return np.array(rows)
    
    def get_config_string(self):
        s = ''
        for i in range(3):
            for j in range(3):
                s += str(self.board[i][j].id)
        return s
    
    @staticmethod
    def read_from_file(file_path: str):
        board = Board()
        Board.Initialize(board)
        if not os.path.exists(file_path):
            raise FileNotFoundError("The path specified does not exist, please check your inputed file location and ensure you are in the right directory.")
        with open(file_path, 'r') as f:
            idx = 0
            for line in f:
                data = []
                for i in line.split(" "):
                    try:
                        i = int(i)
                        data.append(i)
                    except ValueError:
                        pass
                try:
                    board.board[idx][0].id = int(data[0])
                    board.board[idx][1].id = int(data[1])
                    board.board[idx][2].id = int(data[2])          
                except:
                    print("Weird Data Provided:", data)
                idx+=1
        return board


def find_shortest_path(board:'Board'):
    que = HeapQueue()
    initial_path = Path(None, board)
    for action in initial_path.get_actions():
        p = initial_path.step(action)
        que.push(p)
    
    itr = 0
    brch_print = 1 # Modify for changing the printing frequency
    while que.size() > 0:
        itr+=1
        current_path = que.pop()
        if itr % brch_print == 0:
            print('Iteration: ', itr)
            print("Branch Factor:", len(current_path.actions_path))
            print('Length of Queue:', len(que.heap) )

        if not current_path.found_path():
            for action in current_path.get_actions():
                n_path = current_path.step(action)
                if not current_path.is_in_path(n_path.current_state()):  
                    que.push(n_path)
        else:
            return current_path

    return math.inf

def main():
    board = Board.read_from_file('start.txt') # This Line Is editable
    key_to_action = {'w': Actions.UP, 's': Actions.DOWN, 'a': Actions.LEFT, 'd': Actions.RIGHT}

    print(find_shortest_path(board))
    print('Now Feel Free To Play for Yourself!')
    while True: # Lets you play the Game
        print(board.get_configuration())
        key = input('\nEnter Move:')
        key = key_to_action[key.lower()]
        if key:
            board = board.step(key)[0]
    
    
if __name__ == "__main__":
    main()