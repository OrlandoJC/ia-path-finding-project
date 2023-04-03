from astar.search  import AStar

class GraphSearch():
    def __init__(self, environment_matrix, start_point, goal_point):
        self.environment_matrix = environment_matrix
        self.start_point = start_point
        self.goal_point  = goal_point

    def findPath(self):
        return AStar(self.environment_matrix).search(self.start_point, self.goal_point)
    
    def map_path_to_coord(self, path) : 
        pass