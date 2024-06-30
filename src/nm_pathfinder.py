from queue import Queue

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

    boxPath = BFS(source_box, destination_box, mesh["adj"])

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

    # On step 4, implementing A*
    # for converting djikstra to A*, should probably add heuristic to transition_cost
    
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
