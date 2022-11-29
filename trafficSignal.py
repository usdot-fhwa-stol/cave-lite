from threading import Thread
from tkinter import font
import tkinter as tk
import msgIntersect
from time import sleep


class traffic_signal:
  def __init__(self, name, C, offset):
    self.name = name # name used as a label over the top of the signal
    self.C = C # canvas to draw on
    self.offset = offset # position left to right for this instance to draw its light
    name_font = font.Font(family="Helvetica",size=20, weight="bold")
    C.create_text(offset+50,15,font=name_font,text=name)
    C.create_rectangle(offset+0,30,offset+100,370,fill="black")
    C.create_oval(offset+3,40,offset+100,140,fill="gray")
    C.create_oval(offset+3,150,offset+100,250,fill="gray")
    C.create_oval(offset+3,260,offset+100,360,fill="gray")

  def setRed(self):
    self.redLight = self.C.create_oval(self.offset+3,40,self.offset+100,140,fill="red")

  def setYellow(self):
    self.yellowLight = self.C.create_oval(self.offset+3,150,self.offset+100,250,fill="yellow")

  def setGreen(self):
    self.greenLight = self.C.create_oval(self.offset+3,260,self.offset+100,360,fill="green")

  def clearAll(self):
    self.C.delete(self.redLight)
    self.C.delete(self.yellowLight)
    self.C.delete(self.greenLight)

class signal:
  def __init__(self, top):
    self.top = top # hold a window frame
    self.C = tk.Canvas(self.top, bg="white", height=400, width=215)

  def red(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setRed()
    print("red")

  def yellow(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setYellow()
    print("yellow")

  def green(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setGreen()
    print("green")

  def clear(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    print("clear")


def setState():
  while(1):
    updating = msgIntersect.all
    status(msgIntersect.updatingState)
    sleep(0.1)

def status(status):
  if (status == "stop-And-Remain"): 
    state.red()
  elif (status == "protected-Clearance"): 
    state.yellow()
  elif (status == "protected-Movement-Allowed"): 
    state.green()
  else: state.clear()

def loop(top):
  top.mainloop()

print("Starting Traffic Signal\n")
global top
global state
top = tk.Tk() # create a window frame
state = signal(top)
setState()
# s = Thread(target = setState, args=(),  daemon = True)
# s.start()

def main():
  print("outside")
  # t = Thread(target=loop, args=(), daemon=True)
  # t.start()

# main()