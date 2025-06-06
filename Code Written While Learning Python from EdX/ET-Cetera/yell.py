def main():
    yell("this", "is", "CS50")


def yell(*words):
    upeprcased = [word.upper() for word in words]
    print(*upeprcased)

if __name__ == "__main__":
    main()