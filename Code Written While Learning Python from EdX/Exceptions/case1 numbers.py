def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            x = int(input("what's x? "))
        except ValueError:
            print("x is not an interger")
        else:
            break
    return x


main()