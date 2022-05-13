from typing import final
from NYCT import Node

class Path():
    def __init__(self, curr_stop:Node, prev_stop= None, n_transfers_route=0,n_transfers_mode=0):
        self.curr_stop = curr_stop
        self.prev_stop = prev_stop

        self.n_transfer_route = prev_stop.n_transfer_route if prev_stop else 0
        self.n_transfer_mode = prev_stop.n_transfer_mode if prev_stop else 0

    def updateTransfers(self):
        if self.prev_stop:
            if self.curr_stop.transit_type != self.prev_stop.curr_stop.transit_type:
                self.n_transfer_mode +=1

    def observePath(self, solution):
        final_path = [solution[0]]
        to_add = None
        for i in range(1,len(solution)-1):
            start = final_path[-1]
            end = solution[i]

            if not Node.isSame(start, end):
                if to_add:
                    final_path.append(to_add)
                final_path.append(end)
                to_add = None
            else:
                to_add = end
            
        return final_path

    def getPath(self):
        node, history = self,[]
        while node:
            history.append(node)
            node = node.prev_stop
        
        history.reverse()
        solution = [node.curr_stop for node in history[1:]]

        return self.observePath(solution)
