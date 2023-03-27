class EmptyClass:  # Class names are in PascalCase
    pass


# PascalCase
# camelCase
# snake_case
print("No Errors")


# In Python, public attributes can be assigned on-demand to objects:
class User:
    pass


user_1 = User()
user_1.id = '0001'
print(user_1.id)

# For bad indentation fix: Code -> Auto-indent Lines

# A better way to concat strings
print("A""B")
print("This is "
      "much better")
