from tkinter import *

class Nodes:
    """ Used to create nodes for our front end """
    def __init__(self, ix, iy, mycanvas):
        self.connectedEdges = []
        self.adjacent = []
        self.x1 = ix - 25
        self.x2 = ix + 25
        self.y1 = iy - 25
        self.y2 = iy + 25
        self.frontEndID = mycanvas.create_oval(
        self.x1,
        self.y1,
        self.x2,
        self.y2,
        outline="black",
        fill="black",
        tags=("node",),
        )
        self.tag = f"node_{self.frontEndID}"
        mycanvas.addtag(self.tag, "withtag", self.frontEndID)

    #@property
    def centerxy(self, mycanvas):
        """ Return the center x/y coordinate of the node """
        x0, y0, x1, y1 = mycanvas.bbox(self.tag)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        return (cx, cy)

    def addAdjacent(self, node):
        """ Adds adjacent nodes """
        self.adjacent.append(node)

    def addEdges(self, newEdge):
        """ Adds the edge to the connected Edges list """
        self.connectedEdges.append(newEdge)

    def setCenter(self, mycanvas, ix, iy):
        """ sets the x and y coordinates based off a center y """
        self.x1 = ix - 25
        self.x2 = ix + 25
        self.y1 = iy - 25
        self.y2 = iy + 25
        for edges in self.connectedEdges:
            edges.redraw(mycanvas)
    
    def delete(self, mycanvas):
        """ Deletes all edges associated with that node and the graphic of that node"""
        for edges in self.connectedEdges:
            edges.delete(mycanvas, self)
            del edges
        
        mycanvas.delete(self.frontEndID)

    def changeColor(self, mycanvas, color):
        """ Changes the color of the node """
        mycanvas.itemconfig(self.frontEndID, fill=color)
