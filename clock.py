from datetime import datetime
import time
from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont

safe_closing = True
timer_act = False
logs_act = False
file_start = False
process1_after = False
close_requested = False

root = Tk()
root.title("Clock")
root.geometry("800x300")
root.resizable(False, False)


def clock():
    global process1_after
    if not close_requested:
        process1_after = True
        now = datetime.now()
        l1.config(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        aft_id = l1.after(1000, clock)
    else:
        try:
            root.destroy()
        except:
            exit(0)


def on_closing():
    global timer_act
    global close_requested
    global logs_act
    close_requested = True
    timer_act = False
    logs_act = False


def timer(timer_process=True):
    global timer_act
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
    except:
        messagebox.showinfo("Warning!", "Please input the right value")
        b1["text"] = "Start!"
        timer_act = False
        return None
    while temp > -1:
        if not timer_act:
            return None
        else:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            hour.set("{0:02}".format(hours))
            minute.set("{0:02}".format(mins))
            second.set("{0:02}".format(secs))
            root.update()
            time.sleep(1)
            if temp == 0:
                b1["text"] = "Start!"
                timer_act = False
                messagebox.showinfo("Timer", "Time's up ")
            temp -= 1


def timer_click():
    global timer_act
    if not timer_act:
        b1["text"] = "Stop!"
        timer_act = True
        timer()
    elif timer_act:
        b1["text"] = "Start!"
        timer_act = False


def logs_click():
    global logs_act
    if not logs_act:
        logs_button["text"] = "Stop"
        logs_act = True
        calculate_sec()
    elif logs_act:
        logs_button["text"] = "Go!"
        logs_act = False
        file_start = False


def calculate_sec():
    freq = freq_var.get().split()
    seconds = 0
    if freq[1] == "sec":
        seconds = int(freq[0])
    elif freq[1] == "minute" or freq[1] == "minutes":
        seconds = int(freq[0]) * 60
    elif freq[1] == "hour":
        seconds = int(freq[0]) * 3600
    else:
        messagebox.showerror("Error!", "Error! Something with drop list!")
    logsf(seconds)


def logsf(secs):
    global logs_act
    global file_start
    if logs_act:
        now = datetime.now()
        if file_start == False:
            file_start = True
            with open("logs.txt", "w") as file:
                file.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")}\n')
                root.after(secs * 1000, logsf, secs)
        else:
            with open("logs.txt", "a") as file:
                file.write(f'{now.strftime("%Y-%m-%d %H:%M:%S")}\n')
                root.after(secs * 1000, logsf, secs)
    else:
        return None


if safe_closing:
    root.protocol("WM_DELETE_WINDOW", on_closing)

l1 = Label(root, font=("Century Gothic", 30, "bold"), foreground="green")
l1.place(x=210, y=50)

logs_label = Label(root, font=("Century Gothic", 12))
logs_label.config(text="Logs:")
logs_label.place(x=290, y=200)

freq_list = [
    "5 sec",
    "10 sec",
    "30 sec",
    "1 minute",
    "5 minutes",
    "10 minutes",
    "30 minutes",
    "1 hour",
]
freq_var = StringVar(root)
freq_var.set(freq_list[0])
freq = OptionMenu(root, freq_var, *freq_list)
freq.place(x=340, y=200)
logs_button = Button(root, text="Go!", command=logs_click, width=7)
logs_button.place(x=450, y=202)

l2 = Label(root, font=("Century Gothic", 12))
l2.config(text="Timer:")
l2.place(x=275, y=120)
hour = StringVar()
minute = StringVar()
second = StringVar()
hour.set("00")
minute.set("00")
second.set("00")

hEntry = Entry(root, width=3, font=("Century Gothic", 15, ""), textvariable=hour)
hEntry.place(x=340, y=120)

mEntry = Entry(root, width=3, font=("Century Gothic", 15, ""), textvariable=minute)
mEntry.place(x=380, y=120)

sEntry = Entry(root, width=3, font=("Century Gothic", 15, ""), textvariable=second)
sEntry.place(x=420, y=120)

b1 = Button(root, text="Start!", command=timer_click, width=7)
b1.place(x=470, y=120)

clock()


root.mainloop()
