from stack import Stack

priority = {'*': 2, '/': 2, '+': 1, '-': 1, '#': 0}


def middle_to_rp():
    global priority
    rps = []
    try:
        input = open('RP.in', 'r', encoding='utf-8')
        for line in input:
            line = line.strip('\n')
            line = line+'#'
            # print(line)
            ops = Stack()
            ops.push('#')
            rp = ""
            pre = ''
            for char in line:
                if char == '(':
                    ops.push(char)
                elif char == ')':
                    while ops.peek() != '(':
                        if ops.peek() == '#':
                            raise ValueError(char)
                        rp += ops.pop()
                    ops.pop()
                elif char == '#':
                    while ops.peek() != '#':
                        rp += ops.pop()
                        if rp[-1] == '(':
                            raise ValueError(char)
                elif char in priority:
                    if priority[char] > priority[ops.peek()]:
                        ops.push(char)
                    else:
                        while ops.peek() != '(' and priority[ops.peek()] >= priority[char]:
                            rp += ops.pop()
                        ops.push(char)
                else:
                    rp += char
            rps.append(rp)
    except IOError as error:
        print("Failed to open file, error: %s" % error)
    return rps


def compute():
    values = {}
    try:
        input = open('Value.in', 'r', encoding='utf-8')

    except IOError as error:
        print("Failed to open file, error: %s" % error)


if __name__ == '__main__':
    try:
        rps = middle_to_rp()
        for rp in rps:
            print(rp)
    except ValueError as error:
        print("Input error! %s" % error)
