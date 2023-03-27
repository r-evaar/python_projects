import pandas as pd

students = pd.DataFrame({
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
})

print(students)

print('-'*30)
[print(value) for _, value in students.items()]  # Loops along the columns: useless

print('-'*30)
[print(f"[{index}]", row) for index, row in students.iterrows()]

print('-'*30)
print(students['score'].loc[students['student'] == 'Angela'].values[0])

