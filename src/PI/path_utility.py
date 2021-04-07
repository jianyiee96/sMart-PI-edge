import functools, pprint
from collections import deque
import copy

template = [[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 00, 00, 00, 00, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,],
            [ 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00,]]

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

def trace_path(grid: list, path: list, curr_point: Point, next_point: Point):
    
    x_bound = len(grid[0])
    y_bound = len(grid)
    next_step = grid[next_point.y][next_point.x]
    direction = -1

    while(next_step != 0):
        path.append(f"{curr_point.x},{curr_point.y}")

        #check left with priority
        if(curr_point.x - 1 >= 0 and grid[curr_point.y][curr_point.x - 1] == next_step and direction == 1):
            next_step = next_step - 1
            curr_point = Point(curr_point.x - 1, curr_point.y)
            direction = 1
        #check right with priority
        elif(curr_point.x + 1 < x_bound and grid[curr_point.y][curr_point.x + 1] == next_step and direction == 2):
            next_step = next_step - 1
            curr_point = Point(curr_point.x + 1, curr_point.y)
            direction = 2
        #check down with priority
        elif(curr_point.y + 1 < y_bound and grid[curr_point.y + 1][curr_point.x] == next_step and direction == 3):
            next_step = next_step - 1
            curr_point = Point(curr_point.x, curr_point.y + 1)
            direction = 3
        #check up with priority
        elif(curr_point.y - 1 >= 0 and grid[curr_point.y - 1][curr_point.x] == next_step and direction == 4):
            next_step = next_step - 1
            curr_point = Point(curr_point.x, curr_point.y - 1)
            direction = 4
        #check left with priority
        elif(curr_point.x - 1 >= 0 and grid[curr_point.y][curr_point.x - 1] == next_step):
            next_step = next_step - 1
            curr_point = Point(curr_point.x - 1, curr_point.y)
            direction = 1
        #check right
        elif(curr_point.x + 1 < x_bound and grid[curr_point.y][curr_point.x + 1] == next_step):
            next_step = next_step - 1
            curr_point = Point(curr_point.x + 1, curr_point.y)
            direction = 2
        #check down
        elif(curr_point.y + 1 < y_bound and grid[curr_point.y + 1][curr_point.x] == next_step):
            next_step = next_step - 1
            curr_point = Point(curr_point.x, curr_point.y + 1)
            direction = 3
        #check up
        elif(curr_point.y - 1 >= 0 and grid[curr_point.y - 1][curr_point.x] == next_step):
            next_step = next_step - 1
            curr_point = Point(curr_point.x, curr_point.y - 1)
            direction = 4
        
        else:
            return ["Unknown error cause: failed to trace"]
    path.append(f"{curr_point.x},{curr_point.y}")
    return path
                

def bfs(origin: Point, destination: Point, grid: list):

    x_bound = len(grid[0])
    y_bound = len(grid)
    origin_value = x_bound*y_bound

    q = deque()
    q.appendleft(destination)

    while len(q) > 0:
        curr_point = q.pop()
        if(curr_point.y - 1 >= 0):
            if(grid[curr_point.y - 1][curr_point.x] == origin_value):
                return curr_point
            elif(grid[curr_point.y - 1][curr_point.x] == 0):
                q.appendleft(Point(curr_point.x, curr_point.y - 1))
                grid[curr_point.y - 1][curr_point.x] = grid[curr_point.y][curr_point.x] + 1
        #check right
        if(curr_point.x + 1 < x_bound):
            if(grid[curr_point.y][curr_point.x + 1] == origin_value):
                return curr_point
            elif(grid[curr_point.y][curr_point.x + 1] == 0):
                q.appendleft(Point(curr_point.x + 1, curr_point.y))
                grid[curr_point.y][curr_point.x + 1] = grid[curr_point.y][curr_point.x] + 1
        #check down
        if(curr_point.y + 1 < y_bound):
            if(grid[curr_point.y + 1][curr_point.x] == origin_value):
                return curr_point
            elif(grid[curr_point.y + 1][curr_point.x] == 0):
                q.appendleft(Point(curr_point.x, curr_point.y + 1))
                grid[curr_point.y + 1][curr_point.x] = grid[curr_point.y][curr_point.x] + 1
        #check left
        if(curr_point.x - 1 >= 0):
            if(grid[curr_point.y][curr_point.x - 1] == origin_value):
                return curr_point
            elif(grid[curr_point.y][curr_point.x - 1] == 0):
                q.appendleft(Point(curr_point.x - 1, curr_point.y))
                grid[curr_point.y][curr_point.x - 1] = grid[curr_point.y][curr_point.x] + 1
    return None


@functools.lru_cache()
def get_path(ox: int, oy: int, dx: int, dy: int):
    try:
        grid = copy.deepcopy(template)
        print(f"Map dimension: {len(grid[0])}x{len(grid)}")
        x_bound = len(grid[0])
        y_bound = len(grid)

        if(ox == dx and oy == dy):
            print("Same position")
            return ["Same position"]
        elif(ox >= x_bound or dx >= x_bound):
            print("exceed boundaries")
            return ["exceed boundaries"]
        elif(oy >= y_bound or dy >= y_bound):
            print("exceed boundaries")
            return ["exceed boundaries"]
        elif(grid[oy][ox] < 0):
            print("invalid origin point")
            return ["invalid origin point"]
        elif(grid[dy][dx] < 0):
            print("invalid destination point")
            return ["invalid destination point"]
        else:
            grid[dy][dx] = 1
            grid[oy][ox] = x_bound*y_bound

        origin = Point(ox,oy)
        destination = Point(dx,dy)

        print(f"Finding path from ({ox},{oy}) to ({dx},{dy})")

        result = bfs(origin, destination, grid)
        # pprint.pprint(grid)
        
        path = list()
        if(result is not None):
            print("Found path! Tracing path...")
            path = trace_path(grid, path, origin, result)
        else:
            print("Unable to find path.")
        return path
    except:
        return print(["Please supply arguments"])

def apply_path(path: list):
    grid = copy.deepcopy(template)
    path_s = set(path)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(f"{j},{i}" in path_s):
                grid[i][j] = "O"
            elif(grid[i][j] == -1):
                grid[i][j] = "#"
            else:
                grid[i][j] = " "
    # pprint.pprint(grid, width=1000)
    return pprint.pformat(grid, width=1000)