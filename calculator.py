def calc (op, a, b):
    if op == "+":
        return a + b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    elif op == "-":
        return a - b            
    elif op == "%":
        return a % b
    elif op == "^":
        return a ^ b    
a = int(input())
b = int(input())
op = str(input())
print(calc(a, b, op))