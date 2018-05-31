from stack import Stack


def middle_to_rp(inputfile):
    priority = {'(': 3, ')': 3, '*': 2, '/': 2, '+': 1, '-': 1, '~': 1, '#': 0}
    rps = []
    try:
        input = open(inputfile, 'r', encoding='utf-8')
        for line in input:
            line = line.strip('\n')
            line = line+'#'
            # print(line)
            ops = Stack()
            ops.push('#')
            rp = ""
            pre = ''
            for char in line:
                # 预处理 处理正号、负号
                if char == '+':
                    if pre in ['+', '-', '(']:
                        continue
                elif char == '-':
                    if pre in ['+', '-', '(']:
                        char = '~'
                # 求逆波兰式
                if char == '(':
                    ops.push(char)
                elif char == ')':
                    while ops.peek() != '(':
                        if ops.peek() == '#':
                            raise ValueError('( ) must be couple.')
                        rp += ops.pop()
                    ops.pop()
                elif char == '#':
                    while ops.peek() != '#':
                        rp += ops.pop()
                        if rp[-1] == '(':
                            raise ValueError('( ) must be couple.')
                elif char in priority:
                    if priority[char] > priority[ops.peek()]:
                        ops.push(char)
                    else:
                        while ops.peek() != '(' and priority[ops.peek()] >= priority[char]:
                            rp += ops.pop()
                        ops.push(char)
                else:
                    rp += char
                pre = char

            rps.append(rp)
    except IOError as ioerror:
        print("Failed to open file, error: %s" % ioerror)
    except ValueError as verror:
        print("Input error! %s" % verror)

    return rps


def init_var(inputfile):
    values = {}
    try:
        input = open(inputfile, 'r', encoding='utf-8')
        for line in input:
            line = line.strip('\n')
            mors = line.split(';')
            for mor in mors:
                [var, value] = mor.split('=')
                if not value.isdigit():
                    raise ValueError("%s should be digit.")
                if var in values:
                    values[var] = float(value)
                else:
                    values.update({var: float(value)})
    except IOError as ioerror:
        print("Failed to open file, error: %s" % ioerror)
    except ValueError as verror:
        print("Input Error: %s" % verror)

    return values


def compute_rp(rp, values):
    op1 = {'~': lambda x: -x}
    op2 = {'+': lambda y, x: x + y, '-': lambda y, x: x - y,
           '/': lambda y, x: x/y, '*': lambda y, x: x*y}
    res = Stack()
    for char in rp:
        if char in op1:
            assert not res.is_empty()
            res.push(op1[char](res.pop()))
        elif char in op2:
            assert not res.is_empty()
            res.push(op2[char](res.pop(), res.pop()))
        else:
            res.push(values[char])
    assert res.size() == 1
    return res.pop()


if __name__ == '__main__':
    rps = middle_to_rp('RP.in')
    for rp in rps:
        print(rp)
    values = init_var('Values.in')
    print(values)

    print(compute_rp(rp, values))
