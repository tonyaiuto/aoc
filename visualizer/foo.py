#!/usr/bin/env python3


import sys
import threading
import time
import tkinter


class Circle(threading.Thread):

   def __init__(self, root):
     super(Circle, self).__init__()
     self.daemon = False  # cargocult
     self.root = root
     self._done = False

   def run(self):
     canvas = tkinter.Canvas(self.root, bg="white", height=500, width=500)
     coord = 10, 10, 300, 300
     _ = canvas.create_arc(coord, start=0, extent=120, fill="red")
     _ = canvas.create_arc(coord, start=120, extent=215, fill="yellow")
     canvas.pack()

     time.sleep(1)
     _ = canvas.create_arc(coord, start=120, extent=150, fill="blue")
     canvas.pack()
     time.sleep(1)
     _ = canvas.create_arc(coord, start=180, extent=200, fill="green")
     canvas.pack()

     time.sleep(1)
     print("exiting")
     self.root.quit()


root = tkinter.Tk()
c = Circle(root)
c.start()
root.mainloop()
