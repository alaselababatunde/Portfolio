import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument("-n", default=1, type=int, help= "after writing python3 meow.py, you are to parse in '-n' and then 'a number' if you want to meow a couple of times")
args = parser.parse_args()

for _ in range(args.n):
    print ("meow")