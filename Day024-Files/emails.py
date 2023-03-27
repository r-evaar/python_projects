
names_file = "./Input/Names/invited_names.txt"
with open(names_file) as file:
    names = file.readlines()

letter_file = "./Input/Letters/starting_letter.txt"
with open(letter_file) as file:
    letter = file.read()

for name in names:
    name = name.strip()  # Removes pre and post ' ' and '\n'
    filename = f"./Output/ReadyToSend/Invitation - {name}.txt"
    with open(filename, mode='w') as file:
        file.write(letter.replace('[name]', name))
