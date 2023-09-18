from get_soap import getSoapCalMethod

# usage of remote soap service and calculation logic
def calculate(expression):
    if expression == '':
        return '0'

    parts = expression.split(' ')

    # pow first
    i = 0
    while True:
        if parts[i] == '^':
            parts = parts[:i - 1] + [getSoapCalMethod('pow', parts[i - 1], parts[i + 1])] + parts[i + 2:]
        else:
            i += 1
        if i >= len(parts):
            break

    # mul and div next
    i = 0
    while True:
        if parts[i] == '*':
            parts = parts[:i - 1] + [getSoapCalMethod('mul', parts[i - 1], parts[i + 1])] + parts[i + 2:]
        elif parts[i] == '/':
            if parts[i + 1] != '0':
                parts = parts[:i - 1] + [getSoapCalMethod('div', parts[i - 1], parts[i + 1])] + parts[i + 2:]
            else:
                raise ValueError("Division by zero")
        else:
            i += 1
        if i >= len(parts):
            break

    # add and sub
    result = parts[0]
    for i in range(1, len(parts), 2):
        operator = parts[i]
        operand = parts[i + 1]
        if operator == "+":
            result = getSoapCalMethod('add', result, operand)
        elif operator == "-":
            result = getSoapCalMethod('sub', result, operand)
    print(type(result))
    return result