
filename = 'test.txt'
file = open(filename)
content = file.read()

print(content)

file.close()

# Better way:
with open(filename) as file:
    content = file.read()
    print(content)
    # file.write("New line") # Does not work in default r-mode
    # Automatically closes

# modes: a-append, w-write, r-read
with open(filename, mode='a') as file:
    file.write("\nNew line")

new_filename = "new_file.txt"
with open(new_filename, mode='w') as file:
    file.write("Some text")