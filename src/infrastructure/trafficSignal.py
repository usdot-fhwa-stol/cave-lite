from tkinter import *
from tkinter import font
import msgIntersect
import sys

class TrafficSignal:
    def __init__(self, canvas, offset=55):
        self.canvas = canvas
        self.offset = offset
        self.redLight = self.canvas.create_oval(offset+3, 40, offset+100, 140, fill="gray")
        self.yellowLight = self.canvas.create_oval(offset+3, 150, offset+100, 250, fill="gray")
        self.greenLight = self.canvas.create_oval(offset+3, 260, offset+100, 360, fill="gray")
        self.count_font = font.Font(family="Helvetica", size=20, weight="normal")
        self.redText = self.canvas.create_text(self.offset+50, 95, font=self.count_font, text="")
        self.yellowText = self.canvas.create_text(self.offset+50, 205, font=self.count_font, text="")
        self.greenText = self.canvas.create_text(self.offset+50, 315, font=self.count_font, text="")

    def set_color(self, color):
        self.canvas.itemconfig(self.redLight, fill="gray")
        self.canvas.itemconfig(self.yellowLight, fill="gray")
        self.canvas.itemconfig(self.greenLight, fill="gray")
        if color == "red":
            self.canvas.itemconfig(self.redLight, fill="red")
        elif color == "yellow":
            self.canvas.itemconfig(self.yellowLight, fill="yellow")
        elif color == "green":
            self.canvas.itemconfig(self.greenLight, fill="green")

    def set_count(self, color, count):
        self.canvas.itemconfig(self.redText, text="")
        self.canvas.itemconfig(self.yellowText, text="")
        self.canvas.itemconfig(self.greenText, text="")
        if color == "red":
            self.canvas.itemconfig(self.redText, text=count)
        elif color == "yellow":
            self.canvas.itemconfig(self.yellowText, text=count)
        elif color == "green":
            self.canvas.itemconfig(self.greenText, text=count)

class Signal:
    def __init__(self, top):
        self.top = top
        self.canvas = Canvas(self.top, bg="black", height=400, width=215)
        self.canvas.pack()
        self.traffic_signal = TrafficSignal(self.canvas)

    def update_signal(self, state, countdown):
        self.traffic_signal.set_color(state)
        self.traffic_signal.set_count(state, countdown)

def get_state():
    global current_state, countdown
    current_state = msgIntersect.updatingState
    countdown = msgIntersect.countdown

def update():
    get_state()
    if current_state == "stop-And-Remain":
        state.update_signal("red", countdown)
    elif current_state == "protected-clearance":
        state.update_signal("yellow", countdown)
    elif current_state == "protected-Movement-Allowed":
        state.update_signal("green", countdown)
    else:
        state.update_signal("", "")
    top.after(100, update)

def main():
    global top, state
    print("Starting Traffic Signal\n")
    top = Tk()
    state = Signal(top)
    top.after(100, update)
    top.mainloop()

if __name__ == '__main__':
    sys.exit(main())
