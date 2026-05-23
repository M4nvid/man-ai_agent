from functions.write_file import write_file
print("Testing a lorem edit:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("Testing making a new file:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("Testing error catching:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
