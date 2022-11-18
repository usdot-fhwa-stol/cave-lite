from tkinter import font
import tkinter as tk
# from msgIntersect import writeState

class traffic_signal:
  def __init__(self,name,C,offset):
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

class intersection:
  def __init__(self,top):
    self.top = top # hold a window frame
    self.C = tk.Canvas(self.top, bg="white", height=400, width=215)
    self.light={} # hold n traffic signals
    self.light["1"] = traffic_signal("",self.C,55)
    self.C.pack()

    self.light["1"].setRed()

    # Create a statemachine here
    # if (writeState() == "stop-And-Remain") :
    #   self.C.delete(self.greenLight)
    #   self.light["1"].setRed()
    # elif (writeState() == "protected-clearance") :
    #   self.C.delete(self.redLight)
    #   self.light["1"].setYellow()
    # elif (writeState() == "protected-Movement-Allowed") :
    #   self.C.delete(self.yellowLight)
    #   self.light["1"].setGreen()
    # else: self.light["1"].setRed()

# start simulation
print("traffic_signal")
top = tk.Tk() # create a window frame
si = intersection(top) # construct intersection
top.mainloop() # start GUI