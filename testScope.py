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



window.rowconfigure(0, minsize=768, weight=1)
window.columnconfigure(1, minsize=1366, weight=1)
fr_buttons = Frame(window)
# class Display:


class Scope:
    def __init__(self):
        # self.scope = DS1054Z('{}'.format('172.16.3.104'))
        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(111)
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)
        self.textBox = Text(fr_buttons, height=1, width=15)
        self.textBox.grid(row=0, column=1, sticky="ew", padx=5)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, window)  ## here
        self.canvas2 = FigureCanvasTkAgg(self.fig2, window)  ## here
        self.x = np.linspace(0, 6, 1200)

    def connect(self):
        self.inputValue = self.textBox.get("1.0", "end-1c")
        self.scope = DS1054Z('{}'.format(self.inputValue))
        v.set("Connected to :{}".format(self.inputValue))

    def ch1(self):
        self.y1 = self.scope.get_waveform_samples('CHAN1')
        self.ax1.plot(self.x, self.y1)
        self.canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH)
        self.ax1.set_title('DS1054 Channel 1')
        self.read_ch1()

    def ch2(self):
        self.y2 = self.scope.get_waveform_samples('CHAN2')
        self.ax2.plot(self.x, self.y2)
        self.canvas2.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        self.ax2.set_title('DS1054 Channel 2')
        self.read_ch2()

    def read_ch1(self):
        val = self.scope.get_channel_measurement('CHAN1',item='vpp')
        label = Label(lower_frame, font=('Courier', 18), anchor='nw', justify='left',
                      text='Vpp(CH1) : {} V'.format(val))
        label.place(relwidth=1, relheight=1)

    def read_ch2(self):
        val = self.scope.get_channel_measurement('CHAN2', item='vpp')
        label2 = Label(lower_frame1, font=('Courier', 18), anchor='nw', justify='left',
                       text='Vpp(CH2) : {} V'.format(val))
        label2.place(relwidth=1, relheight=1)

    def voltup(self):
        self.canvas1.get_tk_widget().destroy()
        self.__init__()
        self.ax1.set_ylim(-4,4)
        self.ch1()
        self.clicked()

    def voltdown(self):
        self.canvas1.get_tk_widget().destroy()
        self.__init__()
        self.ax1.set_ylim(-2, 2)
        self.ch1()

    def refresh(self):
        self.canvas1.get_tk_widget().destroy()
        self.canvas2.get_tk_widget().destroy()
        self.__init__()
        self.ch1()
        self.ch2()
    def clicked(self,event):
        global clicks
        clicks += 1
        print(clicks)
    # def clear(self):
    #     self.canvas1.get_tk_widget().destroy()
    #     self.canvas2.get_tk_widget().destroy()

if __name__ == '__main__':
    s = Scope()

    canvas = Canvas(window, width=200, height=200)
    canvas.pack(side=BOTTOM, fill=BOTH, expand=1)


    v = StringVar()
    val_ch1 = StringVar()
    val_ch2 = StringVar()
    Label(fr_buttons, textvariable=v).grid(row=0, column=0, sticky="e", padx=5, pady=15)
    Label(fr_buttons, textvariable=val_ch1).grid(row=8, column=3, sticky="e", padx=5, pady=15)
    Label(fr_buttons, textvariable=val_ch2).grid(row=8, column=6, sticky="e", padx=5, pady=15)
    # textBox = Text(fr_buttons, height=1, width=15)
    # textBox.grid(row=0, column=1, sticky="ew", padx=5)
    v.set("IP : ")

    btn_connect = Button(fr_buttons, text="CONNECT", fg="green", command=lambda: s.connect())
    btn_ch1 = Button(fr_buttons, text="CHANNEL 1", fg="blue", command=lambda: s.ch1())
    btn_ch2 = Button(fr_buttons, text="CHANNEL 2", fg="black", command=lambda: s.ch2())
    btn_f5 = Button(fr_buttons, text="REFRESH", fg="black", command=lambda: s.refresh())
    # btn_clr = Button(fr_buttons, text="CLEAR", fg="black", command=lambda: s.clear())
    btn_voltup = Button(fr_buttons, text="INC VOLT/DIV", fg="black",command=lambda: s.voltup())
    btn_voltdown = Button(fr_buttons, text="DEC VOLT/DIV", fg="black",command=lambda: s.voltdown())

    btn_connect.grid(row=0, column=2, sticky="e", padx=5, pady=1)
    btn_ch1.grid(row=1, column=0, sticky="n", padx=5, pady=1)
    btn_ch2.grid(row=1, column=1, sticky="n", padx=5)
    btn_f5.grid(row=1, column=2, sticky="n", padx=5, pady=1)
    # btn_clr.grid(row=1, column=3, sticky="n", padx=5, pady=1)
    btn_voltup.grid(row=2, column=0, sticky="n", padx=5)
    btn_voltdown.grid(row=3, column=0, sticky="n", padx=5)

    fr_buttons.pack(side=TOP, fill=BOTH, expand=1)

    lower_frame = Frame(window, bg='#80c1ff', bd=3)
    lower_frame.place(relx=0.25, rely=0.75, relwidth=0.3, relheight=0.1, anchor='n')

    lower_frame1 = Frame(window, bg='#80c1ff', bd=3)
    lower_frame1.place(relx=0.75, rely=0.75, relwidth=0.3, relheight=0.1, anchor='n')

    window.mainloop()