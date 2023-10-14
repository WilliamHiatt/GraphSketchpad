import tkinter as tk
from nodes import Nodes
from nodes import *
#from main import *

class Edge:

    def __init__(self, n1, n2, isLoop, mycanvas):
        self.n1 = n1
        self.n2 = n2
        if isLoop:
            n1.addEdges(self)
        else:
            n1.addEdges(self)
            n2.addEdges(self)
        self.isParallel = False
        if (n1 in n2.adjacent):
            self.isParallel = True

        n1.addAdjacent(n2)
        n2.addAdjacent(n1)
        self.x1, self.y1 = n1.centerxy(mycanvas)
        self.x2, self.y2 = n2.centerxy(mycanvas)
        self.isLoop = isLoop
        self.isCurved = False



        if self.isLoop:
            self.tag = f"edge__{self.n1.tag}_{self.n2.tag}"
            self.frontEndObject = mycanvas.create_line(self.x1, self.y1, self.x1 - 40, self.y1 - 30, self.x1, self.y1-70, self.x1 + 40, self.y1 - 30, self.x1, self.y1, smooth=1, fill='black')
            mycanvas.addtag(self.tag, "withtag", self.frontEndObject)
            mycanvas.tag_lower(self.tag)
        elif self.isParallel:
            middleX = ((self.x1 + self.x2) / 2) + 30
            middleY = ((self.y1 + self.y2) / 2) - 30
            self.tag = f"edge__{self.n1.tag}_{self.n2.tag}"
            self.frontEndObject = mycanvas.create_line(self.x1, self.y1, middleX, middleY, self.x2, self.y2, smooth=1, fill='black')
            mycanvas.addtag(self.tag, "withtag", self.frontEndObject)
            mycanvas.tag_lower(self.tag)
        else:
            self.tag = f"edge__{self.n1.tag}_{self.n2.tag}"
            self.frontEndObject = mycanvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='black')
            mycanvas.addtag(self.tag, "withtag", self.frontEndObject)
            mycanvas.tag_lower(self.tag)
            self.redraw(mycanvas)


    def redraw(self, mycanvas):
        """ Redraws the edge based on current coordinates of nodes"""
        if self.isLoop:
            self.x, self.y = self.n1.centerxy(mycanvas)
            mycanvas.coords(self.tag, self.x, self.y, self.x - 40, self.y - 30, self.x, self.y-70, self.x + 40, self.y - 30, self.x, self.y)

        elif self.isParallel:
            self.x1, self.y1 = self.n1.centerxy(mycanvas)
            self.x2, self.y2 = self.n2.centerxy(mycanvas)
            middleX = ((self.x1 + self.x2) / 2) + 30
            middleY = ((self.y1 + self.y2) / 2) - 30
            mycanvas.coords(self.tag, self.x1, self.y1, middleX, middleY, self.x2, self.y2)
        else:
            self.x1, self.y1 = self.n1.centerxy(mycanvas)
            self.x2, self.y2 = self.n2.centerxy(mycanvas)
            mycanvas.coords(self.tag, self.x1, self.y1, self.x2, self.y2)

    def delete(self, mycanvas, node):
        """ Deletes the edge on the graphic and removes itself from any connected nodes """
        if node == self.n2:
            self.n1.connectedEdges.remove(self)
        else:
            self.n2.connectedEdges.remove(self)

        mycanvas.delete(self.frontEndObject)

    def isBetween(self, x, y):
        """ Finds if the given coordinate is on the line """
       