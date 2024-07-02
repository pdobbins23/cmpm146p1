from queue import Queue, PriorityQueue
from math import inf, sqrt
import Dijkstra_forward_search as dijkstra

def find_path(source_point, destination_point, mesh):
    path = []
    boxes = {}

    # print(mesh)
    source_box = ();
    destination_box = ();
    for rect in mesh["boxes"]:
        if source_point[1] >= rect[2] and source_point[1] <= rect[3] and source_point[0] >= rect[0] and source_point[0] <= rect[1]:
            if(source_box == ()):
                print(source_point, rect)
                source_box = rect
                if(destination_box != ()):
                    print("both found!")
                    break
        if destination_point[1] >= rect[2] and destination_point[1] <= rect[3] and destination_point[0] >= rect[0] and destination_point[0] <= rect[1]:
            if(destination_box == ()):
                print(destination_point, rect)
                destination_box = rect
                if(source_box != ()):
                    print("both found!")
                    break

    #If there's no start/end point/box
    if source_box == () or destination_box == ():
        print("No path!")
        return path, boxes.keys()

    # boxPath = BFS(source_box, destination_box, mesh["adj"])
    boxPath = AStar(source_box, source_point, destination_box, destination_point, mesh["adj"])

    # print(boxPath)

    if boxPath == None:
        print("No path!")
    else:
        path.append(source_point)
        curPoint = source_point
        lastBox = None
        for box in boxPath:
            boxes[box] = ()
            # For every box after the first,
            # determine a line between the last and the current
            if not lastBox == None:
                curPoint = calcPointLocation(lastBox,curPoint,box)
                path.append(curPoint)
            lastBox = box
        path.append(destination_point)

    # Nearly done with step 4, implementing A*
    # AStar is seemingly slow and inaccurate, test some more and see if it's bugged
    
    return path, boxes.keys()


# Code written by Amit Patel (https://www.redblobgames.com/pathfinding/a-star/introduction.html)
# Performs BFS path search
def BFS(source_box, destination_box, adjDict):
    toVisit = Queue()
    toVisit.put(source_box)
    cameFrom = dict()
    cameFrom[source_box] = None

    while not toVisit.empty():
        current = toVisit.get()
        if(current == destination_box):
            break
        if(current not in adjDict):
            break
        for next in adjDict[current]:
            if next not in cameFrom:
                toVisit.put(next)
                cameFrom[next] = current

    # If not valid path, return none
    if not destination_box in cameFrom:
        print("return None for boxPath")
        return None

    path = [destination_box]
    cur = destination_box

    while cameFrom[cur] != None:
        cur = cameFrom[cur]
        path.insert(0, cur)

    return path

# modified BFS, based off Amit Patel (https://www.redblobgames.com/pathfinding/a-star/introduction.html)
def dijkstra(source_box, source_position, destination_box, destination_position, adjDict):
    toVisit = PriorityQueue()
    toVisit.put(source_box,0)
    toVisitStartPos = Queue()
    toVisitStartPos.put(source_position)
    cameFrom = dict()
    cost_so_far = dict()
    cameFrom[source_box] = None
    cost_so_far[source_box] = 0

    while not toVisit.empty():
        current = toVisit.get()
        currentPoint = toVisitStartPos.get()
        if(current == destination_box):
            break
        if(current not in adjDict):
            break
        for next in adjDict[current]:
            nextPoint = calcPointLocation(current, currentPoint, next)
            new_cost = cost_so_far[current] + distance_cost(currentPoint, nextPoint)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                toVisit.put(next, priority)
                toVisitStartPos.put(nextPoint)
                cameFrom[next] = current

    # If not valid path, return none
    if not destination_box in cameFrom:
        print("return None for boxPath")
        return None

    path = [destination_box]
    cur = destination_box

    while cameFrom[cur] != None:
        cur = cameFrom[cur]
        path.insert(0, cur)

    return path

# modified Djikstra, based off Amit Patel (https://www.redblobgames.com/pathfinding/a-star/introduction.html)
def AStar(source_box, source_position, destination_box, destination_position, adjDict):
    toVisit = PriorityQueue()
    toVisit.put(source_box,0)
    toVisitStartPos = Queue()
    toVisitStartPos.put(source_position)
    cameFrom = dict()
    cost_so_far = dict()
    cameFrom[source_box] = None
    cost_so_far[source_box] = 0

    while not toVisit.empty():
        current = toVisit.get()
        currentPoint = toVisitStartPos.get()
        if(current == destination_box):
            break
        if(current not in adjDict):
            break
        for next in adjDict[current]:
            nextPoint = calcPointLocation(current, currentPoint, next)
            new_cost = cost_so_far[current] + distance_cost(currentPoint, nextPoint)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(destination_position,nextPoint)
                toVisit.put(next, priority)
                toVisitStartPos.put(nextPoint)
                cameFrom[next] = current

    # If not valid path, return none
    if not destination_box in cameFrom:
        print("return None for boxPath")
        return None

    path = [destination_box]
    cur = destination_box

    while cameFrom[cur] != None:
        cur = cameFrom[cur]
        path.insert(0, cur)

    return path

# based off transition_cost from Dijkstra_forward_search.py
def heuristic(goal,next):
    distance = sqrt((goal[0] - next[0])**2 + (goal[1] - next[1])**2)
    return distance

# Taken+modified from Dijkstra_forward_search.py
def distance_cost(cell, cell2):
    distance = sqrt((cell2[0] - cell[0])**2 + (cell2[1] - cell[1])**2)
    return distance

# helper, returns midpoint of box
def midpoint(box): #y1,y2,x1,x2
    print(box)
    return ((box[2] + box[3]) / 2, (box[0] + box[1]) / 2)

#helper, determines where point2 should be
def calcPointLocation(start_box, start_point, end_box):
    y,x = 0,0
    #if end_box to north
    if(start_box[0] == end_box[1]): # s.y1 == e.y2
        print("north")
        y = end_box[1]
        x = min(max(end_box[2], start_point[1]), end_box[3])
    #else if to east
    elif(start_box[3] == end_box[2]): # s.x2 == e.x1
        print("east")
        x = end_box[2]
        y = min(max(end_box[0], start_point[0]), end_box[1])
    #else if to south
    elif(start_box[1] == end_box[0]): # s.y2 == e.y3
        print("south")
        y = end_box[0]
        x = min(max(end_box[2], start_point[1]), end_box[3])
    #else (west)
    elif(start_box[2] == end_box[3]): # s.x1 == e.x2
        print("west")
        x = end_box[3]
        y = min(max(end_box[0], start_point[0]), end_box[1])
    print(str(start_point) + " to " + str(y) + "," + str(x))
    return (y,x)
