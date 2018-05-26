import re
# 1 关键字 2 分界符 3 运算符 4 关系运算符 5 常数 6 标识符 7 字符串 8 单个字符 0 Error
keys = ("include", "define", "char", "double", "enum", "float", "int", "long", "short",
        "signed", "struct", "union", "unsigned", "void", "for",
        "do", "while", "break", "continue", "if", "else", "goto",
        "switch", "case", "default", "return", "auto", "extern",
        "register", "static", "const", "sizeof", "typedef", "volatile")
delimiters = (";", ",", "(", ")", "[", "]", "#", "{", "}")
operators = ("=", "+", "+=", "++", "-", "-=", "--", "*", "*=",
             "/", "/=", "&", "&&", "|", "||", "!", ".", "->", "%", "%=")
relations = ("!=", "==", "<", ">", "<=", ">=")
consts = []
variables = []
strings = []
chars = []

type_table = {1: keys, 2: delimiters, 3: operators,
              4: relations, 5: consts, 6: variables, 7: strings, 8: chars}

ops = (";", ",", "(", ")", "[", "]", "#", "{", "}",
       "=", "+",  "-",  "*", "/", "/=", "&",  "|",  "!",  "%",
       "<", ">")  # '.' 点号单独处理

ops2 = ("+=", "++", "-=", "--", "*=", "&&",
        "||", "->", "%=", "!=", "==", "<=", ">=")

buffer = ""  # 存储当前读取到的子串
peek = ' '  # 存储下一个字符 判断某状态终结时使用
state = 0  # 当前状态
error = "illegal name"


output = open("res.c", "w", encoding="utf-8")


def empty(char):
    global buffer, state, peek, error
    buffer += char
    if char.isalpha() or char == '_':
        if peek.isalpha() or peek == '_' or peek.isdigit():
            state = 2
        else:
            state = 1  # 终态 单个字母或下划线
    elif char.isdigit():
        if peek.isdigit() or peek in ['.', 'l', 'L', 'u', 'U']:
            state = 6
        else:
            state = 5  # 终态 单个数字
    elif char == '.':
        if peek.isdigit():
            state = 6
        elif peek.isalpha() or peek == '_':
            state = 3  # 终态 .号 后跟变量名
        else:
            state = 10  # 错误 .号后有非法字符
            error = "illegal char after '.'"
    elif char == '"':
        state = 8
    elif char == "'":
        state = 10
    elif char in ops:
        if (char + peek) in ops2:
            state = 4
        else:
            state = 3  # 终态 一位符号
    else:
        state = 12  # 终态 错误
        error = "illegal char"


def name(char):
    global buffer, state, peek
    buffer += char
    if peek.isalpha() or peek == '_' or peek.isdigit():
        state = 2
    else:
        state = 1  # 终态 标识符


def op(char):
    global buffer, state
    buffer += char
    state = 3  # 终态 两位符号


def const(char):
    global buffer, state, peek, error
    if char in ['l', 'L', 'u', 'U', 'f', 'F']:
        buffer += char
        state = 5  # 终态 带类型标志的整数或浮点数
    elif char == '.':
        if '.' in buffer:
            state = 12  # 出错 两个小数点
            error = r". is not expected"
        elif peek.isdigit():
            buffer += char
            state = 6
        else:
            buffer += char
            state = 12  # 小数点后无数字跟进 出错
            error = r"digit is expected"
    elif '.' in buffer:  # char is digit 浮点数
        if peek.isdigit() or peek in ['l', 'L', 'f', 'F']:
            buffer += char
            state = 6
        else:
            buffer += char
            state = 5  # 浮点数
    else:  # char is digit 整数
        if peek in ['.', 'l', 'L', 'u', 'U'] or peek.isdigit():
            buffer += char
            state = 6  # 带类型标记的整数
        else:
            buffer += char
            state = 5  # 终态 整数


def string(char):
    global buffer, state, peek
    buffer += char
    if char == '"':
        if buffer[-2] == '\\':
            state = 8  # 有转义符 任何字符都算在字符串内
        else:
            state = 7  # 字符串结束


def single_char(char):
    global buffer, state, peek, error
    buffer += char
    if ('\\' in buffer and len(buffer) > 4) or ('\\' not in buffer and len(buffer) > 3):
        state = 12  # 错误
        error = "too many chars in ''"
    elif char == "'":
        if buffer[-2] == '\\':
            state = 10
        else:
            state = 9  # 终态 单个字符
    # if buffer[1] == '\\':

    #     elif char == "'":
    #         state = 9  # 终态 识别特殊字符
    #     else:
    #         state = 10  # 非终态 转义字符
    # else:
    #     if len(buffer) > 3:
    #         state = 12
    #         error = "too many chars in ''"
    #     elif char == "'":
    #         state = 9  # 终态 单个字符


FSM = {0: empty, 2: name, 4: op, 6: const, 8: string, 10: single_char}


def get_index(id):
    if buffer in type_table[id]:
        index = type_table[id].index(buffer)
    else:
        index = len(type_table[id])
        type_table[id].append(buffer)
    return index


def get_mor(row, line):
    global buffer, state, peek
    if state == 1:
        if buffer in keys:
            id = 1
            index = keys.index(buffer)
        else:
            id = 6
            index = get_index(id)
    elif state == 3:
        if buffer in delimiters:
            id = 2
            index = delimiters.index(buffer)
        elif buffer in operators:
            id = 3
            index = operators.index(buffer)
        else:
            id = 4
            index = relations.index(buffer)
    elif state == 5:
        id = 5
        index = get_index(id)
    elif state == 7:
        id = 7
        index = get_index(id)
    elif state == 9:
        id = 8
        index = get_index(id)
    output.write("%18s" % buffer + "\t\t" + 'at line %d \n' % row)
    buffer = ""
    state = 0
    peek = ' '
    return [id, index]


def scan(line, row):
    global buffer, state, peek, error
    # 去除注释
    line = re.sub(r"(/\*.*\*/)|(//.*$)", '', line)
    line = re.sub(r"(/\*.*$)|(.*\*/)", '', line)
    if line == '':
        return []
    mors = []
    col = 0
    for char in line:
        col += 1
        if col < len(line):
            peek = line[col]
        else:
            peek = ' '
        if state != 8 and state != 10 and (char == ' 'or char == '\t'):
            continue
        FSM[state](char)
        if state % 2 == 1:
            mors.append(get_mor(row, next))
        elif state == 12:
            raise Exception(
                "Syntax error: %s. %s at Line %d, col %d." % (error, buffer, row, col))
    return mors


def main(infile):
    row = 0
    mors = []  # 存储结果 [id, pointer]
    annotate = False  # 标记多行注释
    # 读取文件 并处理
    try:
        input = open(infile, "r", encoding="utf-8")
        for line in input:
            row += 1
            line = line.strip('\n')
            if re.match(r"^ *//.*$", line):  # 单行注释 无代码
                continue
            if not annotate:
                if re.match(r"^.*/\*((?!\*/).)*$", line):
                    annotate = True
                # output.write(line + '\n')
                mors += scan(line, row)
            else:
                if re.match(r"^((?!/\*).)*\*/.*$", line):
                    annotate = False
                    # output.write(line)
                    mors += scan(line, row)
    except IOError as Error:
        print("File Error"+str(Error))
    except Exception as SyntaxError:
        print(str(SyntaxError))


if __name__ == "__main__":
    main("test.c")
