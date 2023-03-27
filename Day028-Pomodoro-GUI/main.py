import tkinter as tk

# ---------------------------- CONSTANTS ------------------------------- #

CLR1 = "#C2DED1"
CLR2 = "#ECE5C7"
CLR3 = "#CDC2AE"
CLR4 = "#354259"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
OFFSET = 5
CHECK = '✔'
TIMER = None

# ---------------------------- TIMER LOOPS --------------------------------------- #
def reset_timer():
    global TIMER
    if TIMER:
        start_btn.after_cancel(TIMER)
    reset_ui()

def reset_ui():
    global itr
    itr = 0
    start_btn.config(state=tk.ACTIVE)
    title_lbl.config(text="Timer", fg=CLR4)
    canvas.itemconfig(timer, text="00:00:00")
    check_lbl.config(text='')

itr = 0
def schedule(canvas_lbl):
    global itr
    itr += 1
    check_lbl.config(text=int(itr/2)*CHECK)  # Work Session completed

    if itr in [1, 3, 5, 7]:
        count_down(canvas_lbl, WORK_MIN * 60)
        title_lbl.config(text="Work", fg="red")
    elif itr in [2, 4, 6]:
        count_down(canvas_lbl, SHORT_BREAK_MIN * 60)
        title_lbl.config(text="Break", fg="purple")
    elif itr == 8:
        count_down(canvas_lbl, LONG_BREAK_MIN * 60)
        title_lbl.config(text="Time Off", fg="green")
    else:
        reset_ui()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def seconds_in_timer(seconds):
    s = int(seconds % 60)
    seconds -= s
    minutes = seconds/60

    m = int(minutes % 60)
    minutes -= m
    hours = minutes / 60

    h = int(hours)

    return f"{h:02d}:{m:02d}:{s:02d}"

def count_down(canvas_lbl, count):
    start_btn.config(state=tk.DISABLED)
    if count >= 0:
        canvas.itemconfig(canvas_lbl, text=seconds_in_timer(count))
        global TIMER
        TIMER = root.after(1000, count_down, canvas_lbl, count-1)
    else:
        schedule(canvas_lbl)


# ---------------------------- UI SETUP ------------------------------- #


root = tk.Tk()
root.title("Pomodoro")

# Get Image info
img_file = 'tomato.png'
img = tk.PhotoImage(file=img_file)
W, H = [img.width(), img.height()]

# Set root dims
PX, PY = W, int(0.75*H)
RW, RH = W+PX, H+PY
root.minsize(RW, RH)
root.maxsize(RW, RH)
root.config(padx=PX/3, pady=PY/8, bg=CLR2)
root.update_idletasks()

# In a Canvas, objects can be overlapped on top of each other
canvas = tk.Canvas(width=W, height=H, bg=CLR2, highlightthickness=0)
#
err = 0  # Image is slightly clipped if canvas boarder is not set to 0 (highlightthickness)
canvas.create_image(W/2+err, H/2-1, image=img)
timer = canvas.create_text(W/2+err, (H/2)*1.2, text="00:00:00", fill="white", font=(FONT_NAME, 25, "bold"))
#
canvas.grid(row=1, column=1)
# canvas.place(relx=0.5, rely=0.5, anchor='center')

title_lbl = tk.Label(text="Timer", font=(FONT_NAME, 30, "bold"), bg=CLR2, fg=CLR4)
# title_lbl.place(relx=0.5, rely=0, anchor='n')
title_lbl.grid(row=0, column=1)

def button(text, width=5, **kw):
    return tk.Button(
        root,
        text=text, width=width,
        takefocus=0, relief='groove',
        borderwidth=0,
        bg=CLR3, fg=CLR4,
        activebackground=CLR1,
        **kw
    )

start_btn = button(text="Start", command=lambda: schedule(timer))
start_btn.grid(row=2, column=0)

reset_btn = button(text="Reset", command=reset_timer)
reset_btn.grid(row=2, column=2)

check_lbl = tk.Label(text='', fg='green', bg=CLR2, font=('Arial', 8, 'bold'))
check_lbl.grid(row=3, column=1)

root.mainloop()
