from NYCT import Node

class Path():
    def __init__(self, curr_stop:Node, prev_stop= None):
        self.curr_stop = curr_stop
        self.prev_stop = prev_stop

    def observePath(self, solution):
        '''Keeps only the two end stops if you have to transfer between multiple stops in the same stations '''
        final_path = [solution[0]]
        to_add = None
        for i in range(1,len(solution)-1):
            start = final_path[-1]
            end = solution[i]

            if not start.isSame(end):
                if to_add:
                    final_path.append(to_add)
                final_path.append(end)
                to_add = None
            else:
                to_add = end   

        if final_path[0].isSame(final_path[1]):
            final_path.pop(0)
        
        if solution[-1] not in final_path:
            final_path.append(solution[-1])
        return final_path

    
    def getPath(self):
        node, history = self,[]
        while node:
            history.append(node.curr_stop)
            node = node.prev_stop
        
        history.reverse()
        solution = [node for node in history]
        if self.curr_stop not in solution:
            solution.append(self.curr_stop)

        return self.observePath(solution)
        # return solution