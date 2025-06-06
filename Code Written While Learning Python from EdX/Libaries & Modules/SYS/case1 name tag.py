import sys

# Check for Errors
if len(sys.argv) < 2:
    sys.exit("Too Few Arguements")
elif len(sys.argv) > 2:
    sys.exit ("Too many Arguements")

#print name tag
print("hello, my name is", sys.argv[1]) 