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

def position_correction(ox: int, oy: int):

    x_bound = len(template[0])
    y_bound = len(template)
    adjustment_strength = 1
    while True:
        if(oy - adjustment_strength >= 0 and template[oy - adjustment_strength][ox] == 0):
            print(f"Successful adjust 1 {ox}, {oy-adjustment_strength}")
            return ox, oy-adjustment_strength
            
        if(oy + adjustment_strength < y_bound and template[oy + adjustment_strength][ox] == 0):
            print(f"Successful adjust 2  {ox}, {oy+adjustment_strength}")
            return ox, oy+adjustment_strength
            
        if(ox - adjustment_strength >= 0 and template[oy][ox - adjustment_strength] == 0):
            print(f"Successful adjust 3  {ox-adjustment_strength}, {oy}")
            return ox-adjustment_strength, oy
            
        if(ox + adjustment_strength < x_bound and template[oy][ox + adjustment_strength] == 0):
            print(f"Successful adjust 4 {ox+adjustment_strength}, {oy}")
            return ox+adjustment_strength, oy
        
        adjustment_strength = adjustment_strength+1

        if(adjustment_strength > x_bound or adjustment_strength > y_bound):
            break
    print("Failed to adjust")
    return ox, oy

def get_path(ox: int, oy: int, dx: int, dy: int):
    try:
        grid = copy.deepcopy(template)
        print(f"Map dimension: {len(grid[0])}x{len(grid)}")
        x_bound = len(grid[0])
        y_bound = len(grid)

        
        if(ox >= x_bound): ox = x_bound-1
        if(dx >= x_bound): dx = x_bound-1
        if(oy >= y_bound): oy = y_bound-1
        if(dy >= y_bound): dy = y_bound-1
        if(ox < 0): ox = 0
        if(dx < 0): dx = 0
        if(oy < 0): oy = 0
        if(dy < 0): dy = 0

        if(ox == dx and oy == dy):
            print("Same position")
            return ["Same position"]
        elif(grid[oy][ox] < 0):
            print("Adjustment required")
            ox, oy = position_correction(ox, oy)
            print(f"New x:{ox} y:{oy}")
        elif(grid[dy][dx] < 0):
            print("invalid destination point")
            return ["invalid destination point"]
            
        grid[dy][dx] = 1
        grid[oy][ox] = x_bound*y_bound
        origin = Point(ox,oy)
        destination = Point(dx,dy)

        print(f"Finding path from ({ox},{oy}) to ({dx},{dy})")

        result = bfs(origin, destination, grid)
        pprint.pprint(grid)
        
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