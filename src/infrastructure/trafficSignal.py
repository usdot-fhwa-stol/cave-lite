from threading import Thread
from tkinter import *
from tkinter import font
from time import sleep
import msgIntersect
import sys


class traffic_signal:
  def __init__(self, C, count = ""):
    global count_font
    offset = 55
    self.count = count # countdown to next signal placed at center of each phase
    self.C = C # canvas to draw on
    self.offset = offset # position left to right for this instance to draw its light
    count_font = font.Font(family="Helvetica",size=20, weight="normal")
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

  def setRedCount(self):
    self.redText = self.C.create_text(self.offset+50,95,font=count_font,text=self.count)
  
  def setYellowCount(self):
    self.yellowText = self.C.create_text(self.offset+50,205,font=count_font,text=self.count)
  
  def setGreenCount(self):
    self.greenText = self.C.create_text(self.offset+50,315,font=count_font,text=self.count)

  def clearAll(self):
    self.C.delete(self.redLight)
    self.C.delete(self.yellowLight)
    self.C.delete(self.greenLight)

  def clearText(self):
    self.C.delete(self.redText)
    self.C.delete(self.yellowText)
    self.C.delete(self.greenText)

class signal:
  def __init__(self, top):
    self.top = top # hold a window frame
    self.C = Canvas(self.top, bg="white", height=400, width=215)

  def redText(self):
    self.light = traffic_signal(self.C, countdown)
    self.C.pack()
    self.light.setRed()
    self.light.setRedCount()

  def yellowText(self):
    self.light = traffic_signal(self.C, countdown)
    self.C.pack()
    self.light.setYellow()
    self.light.setYellowCount()

  def greenText(self):
    self.light = traffic_signal(self.C, countdown)
    self.C.pack()
    self.light.setGreen()
    self.light.setGreenCount()

  def clear(self):
    self.light = traffic_signal(self.C)
    self.C.pack()


def getState():
  global currentState
  global countdown
  while(1):
    currentState = msgIntersect.updatingState
    countdown = msgIntersect.countdown
    setCount()
    sleep(0.1)

def setCount():
  if (currentState == "stop-And-Remain"):
    state.redText()
  elif (currentState == "protected-clearance"):
    state.yellowText()
  elif (currentState == "protected-Movement-Allowed"):
    state.greenText()
  else: state.clear()

def loop(top):
  top.mainloop()

def main():

  print("Starting Traffic Signal\n")
  global top
  global state
  top = Tk() # create a window frame
  state = signal(top)

  stateChangeThread = Thread(target = getState, args=(),  daemon = True)
  stateChangeThread.start()

  loop(top)


if __name__ == '__main__':
  sys.exit(main())
