''' Jonathan Koch
Program Implements A* Pathfinding Algorithm to solve the 8-Tile Game.
'''

from heap_queue import HeapQueue
import math
import os
import numpy as np
from enum import Enum

class Node:
    def __init__(self, state):
        self.state = state
    
class Hexagon:
    '''
        Ajacenct Matrix: Node[i] with Neighbors Node[i][0-5]
    '''
    def __init__(self, ):
        self.state = np.zeros(shape=(6, 6))
        self.current_player = 0
        self.game_depth = 0
        
    def containsTriangle(self,):
        for i in range(4): # Current Node
            for j in range(len(self.state)): #Neighbors
                if self.state[i][j] != 0:
                    if self.__recursiveTriangleSearch(j, self.state[i][j], prev_nodes=[i, j]):
                        a = self.__recursiveTriangleSearch(j, self.state[i][j], prev_nodes=[i, j])
                        return True, self.state[i][j]
        return False, None
    
    def makeConnection(self, x, y, val):
        self.state[x][y] = val
        self.state[y][x] = val
        self.current_player = -val
        self.game_depth += 1
    
    def copy(self):
        new_hex = Hexagon()
        new_hex.state = self.state.copy()
        return new_hex
    
    def get_players_connections(self, player):
        connections = []
        for i in range(6):
            for j in range(len(self.state)):
                if self.state[i][j] == player:
                    a =  [i, j]
                    add = True
                    for s in connections:
                        if set(a).issubset(set(s)):
                            add = False
                        elif set(s).issubset(set(a)):
                                connections.remove(s)
                                
                    if add:
                        connections.append(a)  
        removes = []
        for item in range(len(connections)):
            for item2 in range(len(connections)):
                if item!= item2 and set(connections[item]).issubset(set(connections[item2])):
                    removes.append(connections[item2])
        for item in removes:
            connections.remove(item)
        return connections
          
              
    def __recursiveConnectionSearch(self, current_node, type, prev_nodes=[]):
        for j in range(len(self.state)):
            if self.state[current_node][j] == type and j not in prev_nodes:
                ''' Copy prev nodes and pass to __recursiveTriangleSearch '''
                copy = list(prev_nodes)
                copy.append(j)
                return self.__recursiveConnectionSearch(j, type, prev_nodes=copy)
            
        return prev_nodes
        
        
    def value(self, player, rec=True):
        game_over, winner = self.containsTriangle()
        if winner != None:
            return int(winner == player) * 500 - int(winner != player) * -500
        connections = self.get_players_connections(player)   
        score = self.game_depth
        for con1 in connections:
           for con2 in connections:
               if set(con1).intersection(set(con2)) != set():
                   score += 0.5
        bonus = 0
        ot_connections = self.get_players_connections(-player)
        for c1 in ot_connections:
            for c2 in ot_connections:
                if set(c1).intersection(set(c2)) != set():
                    atmpt_connection = set(c1).union(set(c2))
                    for pot_block in connections:
                        if set(pot_block).issubset(atmpt_connection):
                            bonus+=10

        score += bonus
        if rec:
            score -= self.value(-player, rec=False)
        return score

    def __recursiveTriangleSearch(self, current_node, type, prev_nodes=[]):
        if len(prev_nodes) == 3:
            a, b, c= prev_nodes[0], prev_nodes[1], prev_nodes[2]
            if self.state[a][b] == type and self.state[a][c] == type and self.state[b][c] == type:       
                    return True
            return False
        else:
            for j in range(len(self.state)):
                if j not in prev_nodes and self.state[current_node][j] == type:
                    ''' Copy prev nodes and pass to __recursiveTriangleSearch '''
                    copy = list(prev_nodes)
                    copy.append(j)
                    return self.__recursiveTriangleSearch(j, type, prev_nodes=copy)
            return False

    def get_actions(self):
        actions = []
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if i == j:
                    continue
                if self.state[i][j] == 0:
                    a = [i, j]
                    add = True
                    for s in actions:
                        if set(a).issubset(set(s)):
                            add = False
                    if add:
                        actions.append(a)  
        return actions
    
    def MiniMax(self, player):
        best_value, best_action =  self.__Recursive_MiniMax(self.copy(), 4, player, True)
        # print(f"Agents Best: {best_actions}")
        return best_action
        
    def __Recursive_MiniMax(self, current, depth, player, isMax, alpha=-math.inf, beta=math.inf):
        if depth == 0 or current.containsTriangle()[0]:
                return current.value(player), None
        bestValue = None
        if isMax:
            bestValue = -math.inf
            bestAction = None
            for action in self.get_actions():
                new_current = current.copy()
                new_current.makeConnection(action[0], action[1], player)
                value, _ = self.__Recursive_MiniMax(new_current, depth-1, player, False, alpha, beta)
                oldBest = bestValue
                bestValue = max(bestValue, value)
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
                if bestValue != oldBest:
                    bestAction = action
            return bestValue, bestAction
        else:
            bestValue = math.inf
            bestAction = None
            for action in self.get_actions():
                new_current = current.copy()
                new_current.makeConnection(action[0], action[1], -player)
                value,_ = self.__Recursive_MiniMax(new_current, depth-1, player, True, alpha, beta)
                oldBest = bestValue
                bestValue = min(bestValue, value)
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestValue, None
        
        
    
def main():

    h = Hexagon()
    current_player = 1
    your_player = int(input("Enter your player:(1/-1) "))
    
    while True:
        print('Possible Actions: ', h.get_actions())
        print('Your Connections:', h.get_players_connections(your_player))
        print('Agent\'s Connections:', h.get_players_connections(-your_player))
        if your_player == current_player:
            try:
                move = input("Enter your move ie. 3 4 ...").split()
                h.makeConnection(int(move[0]), int(move[1]), current_player)
            except:
                print("Invalid input. You lose...")
                exit(2)
        else:
            agent_move = h.MiniMax(current_player)
            h.makeConnection(agent_move[0], agent_move[1], current_player)
            print(f'Agent Move: {agent_move[0]} {agent_move[1]}')
        
        print('Your Score:', h.value(your_player))
        
        win = h.containsTriangle()
        if win[0]:
            print(f"Player {win[1]} wins!")
            exit(0)
        current_player*=-1
        
        # input("Hit Enter to continue...")
        
    
    
    
if __name__ == "__main__":
    main()