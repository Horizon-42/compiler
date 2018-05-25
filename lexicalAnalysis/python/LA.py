import re
# 1 关键字 2 分界符 3 运算符 4 关系运算符 5 常数 6 标识符 0 Error
keys = ("char", "double", "enum", "float", "int", "long", "short",
        "signed", "struct", "union", "unsigned", "void", "for",
        "do", "while", "break", "continue", "if", "else", "goto",
        "switch", "case", "default", "return", "auto", "extern",
        "register", "static", "const", "sizeof", "typedef", "volatile")
delimiters = (";", ",", "(", ")", "[", "]")  # state 5,6,7,8,9,10
#            11   12   13     15  16    18   19
operators = ("=", "+", "+=", "-", "-=", "*", "*=",
             #            21   22    24    25   27   28    30   31   32
             "/", "/=", "&", "&&", "|", "||", "!", ".", "->")
relations = ("!=", "==", "<", ">", "<=", ">=")
consts = []
variables = []

type_table = {1: keys, 2: delimiters,
              3: operators, 4: relations, 5: consts, 6: variables}

output = open("clean_code.c", "w", encoding="utf-8")


def check(state, morphere):  # 获取二元词素
    assert state > 0
    try:
        pointer = type_table[id].index(morphere)
    except ValueError as Error:
        if id < 5:
            pointer = len(type_table[id])
            type_table[id] += [morphere]
        else:
            print("Wrong input: "+Error)
    return [id, pointer]


one_op = [";", ",", "(", ")", "[", "]", "."]
two_op = ["=", "+", "-", "*", "/", "&", "|", "!", "<", ">"]

# R = {0: empty, 1: name, 2: num, 3:string, 4:achar, 5: op, 6: ops, 7: end} # 8 表示错误


def empty(char):
    if char.isalpha() or char == '_':
        return 1
    elif char.isdigit():
        return 2
    elif char == '"':
        return 3
    elif char == "'":
        return 4
    elif char in one_op:
        return 5
    elif char in two_op:
        return 6
    return 8  # error


def name(char):
    if char.isalpha() or char.isdigit() or char == '_':
        return 1
    else:
        return 0


def num(char):
    state = 0
    return state


def string(char):
    return 0


def achar(char):
    return 0


def op(char):
    state = 0
    return state


def ops(char):
    return 0


def end(char):
    return 0


R = {0: empty, 1: name, 2: num, 3: string, 4: achar, 5: op, 6: ops, 7: end}


def FSM(word, col):
    morphere = []
    start = 0  # 标记词素的起始位置
    end = 0  # 标记词素的结束
    state = 0  # 标记词素类型 0为空
    for char in word:
        state = R[state](char)
        if state == 0:
            morphere.append(check(state, word[start:end]))
            start = end  # 遍历下一个词素
        elif state == 8:
            pass  # 处理错误
        else:
            end += 1


def line_to_words(line, row):
    # pre process 去除注释、空行
    morphere = []
    line = line.strip(' ')
    line = re.sub(r"(/\*.*\*/)|(//.*$)", '', line)
    line = re.sub(r"(/\*.*$)|(.*\*/)", '', line)
    line = re.sub(r"  *", ' ', line)
    #itrs = re.finditer(r"(/\*.*\*/)|(//.*$)|(/\*.*$)|(.*\*/)", line)
    # for i in itrs:
    #     print(i)
    if(line == ''):
        return []
    if(re.match(r"^#include *<.*>.*$", line)):
        line = re.sub(r"^#include *<.*> *", ',', line)
    words = line.split()
    col = 0
    for word in words:
        morphere += FSM(word, col)
        col+len(word)
    output.write(line+'\n')
    return morphere


def main(infile):
    row = 0
    morphere = []  # 存储结果 [id, pointer]
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
                morphere += line_to_words(line, row)
            else:
                if re.match(r"^((?!/\*).)*\*/.*$", line):
                    annotate = False
                    morphere += line_to_words(line, row)

    except IOError as Error:
        print("File Error"+str(Error))


if __name__ == "__main__":
    main("test.c")
