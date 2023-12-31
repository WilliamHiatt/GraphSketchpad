import tkinter as tk
from nodes import *

class Canvas(tk.Frame):
    """Class that is used to control our canvas"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = tk.Canvas(width=800, height=600, background="White")
        self.canvas.grid(row=1, column=1)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        self.create_node(100, 100, "white")
        self.create_node(200, 100, "black")

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("node", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("node", "<B1-Motion>", self.drag)

    def create_node(self, x, y, color):
        """Create a token at the given coordinate in the given color"""
        self.canvas.create_oval(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            outline=color,
            fill=color,
            tags=("node",),
        )

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def createNodeMode(self, event):
        self.canvas.bind("<ButtonPress-1>", self.create_node(event.x, event.y, "Black"))



if __name__ == "__main__":
    root = tk.Tk()
    newCanvas = Canvas(root).grid(row=1, column=1)
    nodeButton = tk.Button(root, text="Create New Node", bd="5", command=newCanvas.createNodeMode())
    root.mainloop()