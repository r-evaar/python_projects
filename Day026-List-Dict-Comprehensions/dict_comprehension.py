from random import randint
import pandas as pd

# new_dict = {new_key:new_value for item in list if test}

names = ['Alex', 'Beth', 'Caroline', 'Dave', 'Eleanor', 'Freddie']
gen_score = lambda: randint(50, 100)

students_scores = {name: gen_score() for name in names}
print(pd.Series(students_scores))

passed_students = {name: score for name, score in students_scores.items() if score > 70}
print(passed_students)
