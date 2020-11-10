import tkinter
from tkinter import *
from ds1054z import DS1054Z
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
plt.style.use('seaborn-whitegrid')

window = Tk()
window.title('DS1054Z App')
# window.iconbitmap('')
window.geometry("1366x768")

clicks = 0
fig1 = Figure()
ax1 = fig1.add_subplot(111)
fig2 = Figure()
ax2 = fig2.add_subplot(111)

window.rowconfigure(0, minsize=768, weight=1)
window.columnconfigure(1, minsize=1366, weight=1)


# class Display:


class Scope:
    def __init__(self):
        # self.scope = DS1054Z('{}'.format('172.16.3.104'))
        self.fr_buttons = Frame(window)
        self.textBox = Text(self.fr_buttons, height=1, width=15)
        self.textBox.grid(row=0, column=1, sticky="ew", padx=5)

    def connect(self):
        self.inputValue = self.textBox.get("1.0", "end-1c")
        self.scope = DS1054Z('{}'.format(self.inputValue))
        v.set("Connected to :{}".format(self.inputValue))

    def ch1(self):
        global fig1, ax1,clicks
        x = np.linspace(0, 6, 1200)
        y1 = (self.scope.get_waveform_samples('CHAN1'))

        # y1 = np.sin(x)
        ax1.plot(x, y1, range(0, 1))
        # canvas1 = FigureCanvasTkAgg(fig1, master=graph)
        # canvas1.get_tk_widget().pack()
        # canvas1.show()
        canvas1 = FigureCanvasTkAgg(fig1, window)  ## here
        canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH)
        # canvas1.draw()
        # plt.plot(x,y2)
        ax1.set_title('DS1054 Channel 1')
        plt.show()
        # clicks += 1
        # if clicks % 2 == 0:
        #     canvas1.withdraw()
        # else:
        #     graph.deiconify()

    def ch2(self):
        global fig2, ax2
        y2 = (self.scope.get_waveform_samples('CHAN2'))
        x = np.linspace(0, 6, 1200)
        # y2 = np.cos(x)
        # ax1.plot(x, y1)
        ax2.plot(x, y2, range(0, 1))
        canvas2 = FigureCanvasTkAgg(fig2, window)  ## here
        # canvas.show()
        canvas2.get_tk_widget().pack(side=LEFT, fill=BOTH)
        ax2.set_title('DS1054 Channel 2')
        plt.show()

    def voltup(self):
        global clicks, fig1, ax1  # this will use the variable to count
        clicks = clicks + 1
        # plt.ylim(0,1+clicks)
        ymax = plt.ylim()
        plt.ylim(0, ymax * clicks)

    def voltdown(self):
        global clicks, fig1, ax1  # this will use the variable to count
        clicks = clicks - 1
        ax1.ylim(0, 5 - clicks)


if __name__ == '__main__':
    s = Scope()

    canvas = Canvas(window, width=200, height=200)
    canvas.pack(side=BOTTOM, fill=BOTH, expand=1)


    v = StringVar()
    Label(s.fr_buttons, textvariable=v).grid(row=0, column=0, sticky="e", padx=5, pady=15)
    # textBox = Text(fr_buttons, height=1, width=15)
    # textBox.grid(row=0, column=1, sticky="ew", padx=5)
    v.set("IP : ")

    btn_connect = Button(s.fr_buttons, text="CONNECT", fg="red", command=lambda: s.connect())
    btn_ch1 = Button(s.fr_buttons, text="CHANNEL 1", fg="blue", command=lambda: s.ch1())
    btn_ch2 = Button(s.fr_buttons, text="CHANNEL 2", fg="black", command=lambda: s.ch2())
    # btn_voltup = Button(fr_buttons, text="INC VOLT/DIV", fg="black",command=lambda: voltup())
    # btn_voltdown = Button(fr_buttons, text="DEC VOLT/DIV", fg="black",command=lambda: voltdown())

    btn_connect.grid(row=0, column=2, sticky="n", padx=5, pady=1)
    btn_ch1.grid(row=1, column=0, sticky="n", padx=5, pady=1)
    btn_ch2.grid(row=1, column=1, sticky="n", padx=5)
    # btn_voltup.grid(row=2, column=0, sticky="n", padx=5)
    # btn_voltdown.grid(row=3, column=0, sticky="n", padx=5)

    s.fr_buttons.pack(side=TOP, fill=BOTH, expand=1)

    window.mainloop()