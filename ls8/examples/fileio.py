import sys
# open a filename
# try:
#     f = open("print8.ls8", "r")
#     lines = f.read()
#     print(lines)

#     raise Exception("hi")
# except:
#     print(f.closed)
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print("remember to pass the file name as an argument")
    sys.exit()

try:
    with open(filename, "r") as f:
        for line in f:
            possible_number = line[:line.find("#")]
            if possible_number == "":
                continue
            regular_int = int(possible_number, 2)
            print(regular_int)
    
except FileNotFoundError:
    print(f"We did not find file {filename}")

