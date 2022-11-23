from threading import Thread
from tkinter import font
import tkinter as tk
from msgIntersect import main

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
  def __init__(self, top, currentState):
    self.top = top # hold a window frame
    self.C = tk.Canvas(self.top, bg="white", height=400, width=215)
    # self.light = traffic_signal("",self.C,55)
    # self.C.pack()

    # self.C.after(2000, self.red)
    if (currentState == "stop-And-Remain") : 
      self.red
    elif (currentState == "protected-Clearance") : 
      self.yellow
    elif (currentState == "protected-Movement-Allowed") : 
      self.green
    else: self.clear

  def red(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setRed()

  def yellow(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setYellow()

  def green(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()
    self.light.setGreen()

  def clear(self):
    self.light = traffic_signal("",self.C,55)
    self.C.pack()

def status(main):
  status = main
  return status

print("Starting Traffic Signal\n")
top = tk.Tk() # create a window frame
def gen(top):
  # start simulation
  print(status())
  signal(top, status())

def loop(top):
  top.mainloop() # start GUI

try:
  s = Thread(target = status, args=(main()),  daemon = True) 
  s.start()
except:
  print("Something didn't work in retrieving status.")

try:
  t = Thread(target = status, args=(top),  daemon = True) 
  t.start()
except:
  print("Something didn't work in generation.")

loop(top)