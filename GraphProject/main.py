from tkinter import *
from edges import Edge
from nodes import *
from edges import *

nodesAndEdgesDict = {}
firstNode = None
numNodes = 0
numEdges = 0

drag_data = {"x": 0, "y": 0, "item": None}
selected_node = {"x": 0, "y": 0, "item": None}

root = Tk()
root.title("Graph Theory Program")
root.geometry("800x600")
root.configure(bg="Grey")


w = 1320
h = 840
x = w/2
y = h/2

def unbindAll():
    mycanvas.unbind('<ButtonPress-1>')
    mycanvas.unbind('<ButtonRelease-1>')
    mycanvas.unbind("<B1-Motion>")


def unbindTags():
    mycanvas.tag_unbind("node", "<ButtonPress-1>")
    mycanvas.tag_unbind("node", "<ButtonRelease-1>")
    mycanvas.tag_unbind("node", "<B1-Motion>")

def mouseLocation(event):
    return (event.x, event.y)

def create_node(event):
    """Create a node at the given coordinate in the given color"""
    x = event.x
    y = event.y

    tempNode = Nodes(x, y, mycanvas)
    nodesAndEdgesDict[tempNode] = tempNode.connectedEdges
    global numNodes
    numNodes += 1
    updateCounts()


def create_edge(event):
    """Create a edge at the given coordinate in the given color"""
    x = event.x
    y = event.y
    global firstNode
    global numEdges

    if firstNode == None:
        firstNode = getNodeAtLocation(x, y)
        if firstNode == None:
            myLabel['text']= "Select the first node."
        else:
            myLabel['text']= "Select the second node."
    
    elif isinstance(firstNode, Nodes):
        secondNode = getNodeAtLocation(x, y)
        if secondNode != None:
            if firstNode == secondNode:
                tempEdge = Edge(firstNode, secondNode, True,mycanvas)
                firstNode = None
                myLabel['text']= "Select the first node."
            else:
                tempEdge = Edge(firstNode, secondNode, False, mycanvas)
                firstNode = None
                myLabel['text']= "Select the first node."
        else:
            myLabel['text']= "Select the second node."
        numEdges += 1
        updateCounts()


def updateCounts():
    """ Updates the number of edges and nodes displayed """
    nodeCountLabel.config(text= "Number of Nodes: " + str(numNodes))
    edgeCountLabel.config(text="Number of Edges." + str(numEdges))

def delete_node(event):
    """ Deletes the node at the location of the button click """
    global numEdges
    node = getNodeAtLocation(event.x, event.y)
    numEdges -= len(node.connectedEdges)
    node.delete(mycanvas)
    del node
    global numNodes
    numNodes -= 1
    updateCounts()
    
def getNodeAtLocation(x, y):
    """ Finds the node at the given location """
    for key in nodesAndEdgesDict:
        if (key.x1 <= x and key.x2 >= x) and (key.y1 <= y and key.y2 >= y):
            return key

def delete_edge(event):
    edge = getEdgeAtLocation(event.x, event.y)
    edge.delete(mycanvas, edge.n1)

def getEdgeAtLocation(x, y):
    mycanvas.find_closest

def newNodeButtonClick():
    """ Goes into this mode once the new node button has been clicked. """
    myLabel['text']= "Click on the Canvas to Place Nodes."
    unbindTags()
    mycanvas.bind('<ButtonPress-1>', create_node)

def newEdgeButtonClick():
    """ Goes into this mode once the new node button has been clicked. """
    myLabel['text']= "Select the first node."
    unbindTags()
    mycanvas.bind('<ButtonPress-1>', create_edge)

def deleteNodesButtonClick():
    """ Deletes a node when it's selected """
    myLabel['text']= "Click a node to delete it."
    unbindAll()
    unbindTags()
    mycanvas.bind('<ButtonPress-1>', delete_node)

def deleteEdgesButtonClick():
    """ Deletes a node when it's selected """
    myLabel['text']= "Click a edge to delete it."
    unbindAll()
    unbindTags()
    mycanvas.bind('<ButtonPress-1>', delete_edge)

def color(event):
    """ Gets the color and changes the node """
    tempNode = getNodeAtLocation(event.x, event.y)
    newColor = textBox.get(1.0, "end-1c")
    tempNode.changeColor(mycanvas, newColor)
    

def changeColor():
    """ Changes node so that it's red """
    myLabel['text']= "Click a node to change it's color."
    unbindAll()
    unbindTags()
    mycanvas.bind('<ButtonPress-1>', color)

def move():
    myLabel['text']= "Click and hold to drag a node."
    unbindAll()
    mycanvas.tag_bind("node", "<ButtonPress-1>", drag_start)
    mycanvas.tag_bind("node", "<ButtonRelease-1>", drag_stop)
    mycanvas.tag_bind("node", "<B1-Motion>", drag)

def drag_start(event):
    """Begining drag of an object"""
    # record the item and its location
    drag_data["item"] = mycanvas.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def drag_stop(event):
    """End drag of an object"""
    # reset the drag information
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0

def drag(event):
    """Handle dragging of an object"""
    # compute how much the mouse has moved
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    # move the object the appropriate amount
    mycanvas.move(drag_data["item"], delta_x, delta_y)
    # record the new position
    drag_data["x"] = event.x
    drag_data["y"] = event.y
    for key in nodesAndEdgesDict:
        if key.frontEndID == drag_data["item"]:
            key.setCenter(mycanvas, event.x, event.y)
            #for edges in nodesAndEdgesDict[key]:
            #    edges.redraw(mycanvas)


mycanvas = Canvas(root, width=w, height=h, bg="white")
mycanvas.place(x = 150, y = 30)


newNodeButton = Button(root, text="Create New Node", bd="5", command=newNodeButtonClick)
newNodeButton.place(x = 10, y = 10)


newEdgeButton = Button(root, text="Create New Edge", bd="5", command=newEdgeButtonClick)
newEdgeButton.place(x = 10, y = 45)


moveNodeButton = Button(root, text="Move Nodes", bd="5", command=move)
moveNodeButton.place(x=10, y = 80)

deleteNodeButton = Button(root, text="Delete Nodes", bd="5", command=deleteNodesButtonClick)
deleteNodeButton.place(x=10, y = 115)

deleteEdgeButton = Button(root, text="Delete Edges", bd="5", command=deleteEdgesButtonClick)
deleteEdgeButton.place(x=10, y = 150)

colorRed = Button(root, text="Change Node Color", bd="5", command=changeColor)
colorRed.place(x=10, y=185)

textBox = Text(root, height = 1, width= 15)
textBox.place(x=10, y=225)

myLabel = Label(root, text="")
myLabel.place(x=810, y=870)

nodeCountLabel = Label(root, text="Number of Nodes: " + str(numNodes))
nodeCountLabel.place(x=150, y=5)

edgeCountLabel = Label(root, text="Number of Edges: " + str(numEdges))
edgeCountLabel.place(x=350, y=5)


root.mainloop()