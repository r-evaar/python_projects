from html import unescape

class Question:

    def __init__(self, q_text, q_answer):
        self.text = unescape(q_text)
        self.answer = True if unescape(q_answer) == 'True' else False
