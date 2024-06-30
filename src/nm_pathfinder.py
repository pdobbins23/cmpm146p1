from queue import Queue

def find_path(source_point, destination_point, mesh):
    path = []
    boxes = {}

    # print(mesh)
    source_box = ();
    destination_box = ();
    for rect in mesh["boxes"]:
        if source_point[0] >= rect[0] and source_point[0] <= rect[1] and source_point[1] >= rect[2] and source_point[1] <= rect[3]:
            if(source_box == ()):
                print(source_point, rect)
                source_box = rect
                if(destination_box != ()):
                    print("both found!")
                    break
        if destination_point[0] >= rect[0] and destination_point[0] <= rect[1] and destination_point[1] >= rect[2] and destination_point[1] <= rect[3]:
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

    print(boxPath)

    if boxPath == None:
        print("No path!")
    else:
        for box in boxPath:
            path.append(midpoint(box))
            boxes[box] = ()
    
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
def midpoint(box): #x1,x2,y1,y2
    print(box)
    return ((box[0] + box[1]) / 2, (box[2] + box[3]) / 2)
