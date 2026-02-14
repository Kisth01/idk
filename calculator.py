def calc (op, a, b):
    
    if op == "+":
        print(a + b)
    elif op == "*":
        print(a * b)
    elif op == "/":
        print(a / b)
    elif op == "//":
        print(a // b)
    elif op == "-":
        print(a - b)          
    elif op == "%":
        print(a % b)
    elif op == "^":
        print(a ^ b)    
a = int(input())
b = int(input())
op = str(input())
calc(op, a, b)