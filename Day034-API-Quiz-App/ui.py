import tkinter as tk
from utils import button
from quiz_brain import QuizBrain

CLR_BG = "#375362"
W, H = 400, 500
BTN_R = 1.25
FONT_Q = ('Arial', 20, 'italic')
FONT_S = ('Calibri', 15, 'bold')
C_W, C_H = 300, 250

class QuizUI:

    def __init__(self, quiz: QuizBrain):

        # --- UI Definitions ------------------ #
        self.root = tk.Tk()
        self.q_canvas = tk.Canvas(width=C_W, height=C_H)
        self.t_btn, self.t_btn_r, self.t_btn_c = \
            button(
                ratio=BTN_R,
                img_file={'release': './images/true_n.png', 'press': './images/true_a.png'}
            )
        self.f_btn, self.f_btn_r, self.f_btn_c = \
            button(
                ratio=BTN_R,
                img_file={'release': './images/false_n.png', 'press': './images/false_a.png'}
            )
        self.question = self.q_canvas.create_text(C_W / 2, C_H / 2, font=FONT_Q)
        self.score = tk.Label(text='Score: 0', font=FONT_S)

        # --- Attributes ---------------------- #
        self.root.is_running = True
        self.quiz = quiz

        # --- Configuration ------------------- #
        x = int(self.root.winfo_screenwidth()/2 - W/2)
        y = int(self.root.winfo_screenheight()/2 - H/2)
        self.root.title("Quizzler")
        self.root.geometry(f"{W}x{H}+{x}+{y}")
        self.root.configure(bg=CLR_BG)

        self.q_canvas.configure(bg='white', highlightthickness=0)
        self.q_canvas.itemconfig(self.question, width=C_W*0.9)

        self.t_btn.configure(bg=CLR_BG, activebackground=CLR_BG)
        self.f_btn.configure(bg=CLR_BG, activebackground=CLR_BG)

        self.score.configure(bg=CLR_BG, fg='white', anchor='e')

        # --- Rendering ----------------------- #
        x, y = 0.5, 0.38
        self.q_canvas.place(relx=x, rely=y, anchor='center')

        x = (W-self.q_canvas.winfo_reqwidth())/(2*W)
        y += 0.42
        self.t_btn.place(relx=x, rely=y, anchor='w')
        self.f_btn.place(relx=1-x, rely=y, anchor='e')

        self.score.place(relx=1-x, rely=0.07, anchor='e')

        # --- Callbacks ----------------------- #
        self.t_btn.configure(command=lambda: self.btn_clicked(True))
        self.f_btn.configure(command=lambda: self.btn_clicked(False))

        # --- Threading ----------------------- #


        # --- Startup ------------------------- #
        self.update_question()
        self.root.mainloop()

    def update_question(self):
        text = self.quiz.next_question()
        self.q_canvas.itemconfig(self.question, text=text)

    def btn_clicked(self, tf):
        answer_is_correct = tf == self.quiz.current_question.answer
        self.process_ans(answer_is_correct)

    def process_ans(self, tf):

        if tf:
            color = 'green'
            self.quiz.score += 1
            self.score.configure(text=f"Score: {self.quiz.score}")
        else:
            color = 'red'

        self.q_canvas.configure(bg=color)
        self.t_btn.configure(state=tk.DISABLED)
        self.f_btn.configure(state=tk.DISABLED)
        self.q_canvas.after(1000, self.next)

    def next(self):
        end = self.check_status()
        if end: return
        self.q_canvas.configure(bg='white')
        self.t_btn.configure(state=tk.NORMAL)
        self.f_btn.configure(state=tk.NORMAL)
        self.update_question()

    def check_status(self):
        n = len(self.quiz.question_list)
        if n == self.quiz.question_number:
            end = True
            self.q_canvas.configure(bg='white')
            txt = f"Your final score is: {self.quiz.score}"
            self.q_canvas.itemconfig(self.question, text=txt)
        else:
            end = False

        return end

