
# def add(a, b):
#     return a+b

def add_numbers(a, b):
    sum = a + b
    print("The sum of", a, "and", b, "is:", sum)
    return su  # Typo here: Should be 'sum'

def main():
    result = add_numbers(10, "20")  # TypeError: Adding int and str
    print("Result:", result)

if __name__ == "__main__":
    main()
