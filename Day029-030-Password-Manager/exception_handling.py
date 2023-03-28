# try:
#   code that might fail
# except:
#   if it fails
# else:
#   if it doesn't fail
# finally:
#   run regardless

def foo():
    try:
        a_dictionary = {'key': 'value'}
        print(a_dictionary['another_key'])
        file = open('file.txt', 'r')
    except FileNotFoundError:
        print("File not found.")
        return
    except KeyError as key:
        print(f"Key {key} not found.")
        return
    else:
        print("File found.")
        file.close()
    finally:
        print("Clean up.")

foo()

raise InterruptedError("This is an error because your input is shit")
