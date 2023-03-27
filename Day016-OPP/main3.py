from prettytable import PrettyTable

table = PrettyTable()

col_names = ['Pokemon Name', 'Type']
col_data = [
    ['Pikachu', 'Squirtle', 'Charmander'],
    ['Electric', 'Water', 'Fire']
]

for name, data in zip(col_names, col_data):
    table.add_column(name, data)

table.align = "l"

print(table)
