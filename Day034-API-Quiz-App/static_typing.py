x: int
x = 12
print(x)

# Helpful for detecting bugs
def police_check(age: float) -> bool:
    if age > 18:
        can_drive = True
    else:
        can_drive = False
    return can_drive

print(f"Can drive? {police_check(19)}")
