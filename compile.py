import sys
import os

if len(sys.argv) == 1 or sys.argv[1] == "seperate":
	os.system("make seperate compiled=0")
elif sys.argv[1] == "map":
	os.system("make maps")
elif sys.argv[1] == "clean":
	os.system("make clean")
else:
	os.system("make compiled compiled=1")
