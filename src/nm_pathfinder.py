def find_path(source_point, destination_point, mesh):
    path = []
    boxes = {}

    # print(mesh)
    source_box = ();
    destination_box = ();
    for rect in mesh["boxes"]:
        if source_point[0] >= rect[0] and source_point[0] <= rect[1] and source_point[1] >= rect[2] and source_point[1] <= rect[3]:
            print(source_point, rect)
            source_box = rect
            if(destination_box != ()):
                print("both found!")
                break
        if source_point[0] >= rect[0] and source_point[0] <= rect[1] and source_point[1] >= rect[2] and source_point[1] <= rect[3]:
            print(source_point, rect)
            destination_box = rect
            if(source_box != ()):
                print("both found!")
                break
    
    return path, boxes.keys()
