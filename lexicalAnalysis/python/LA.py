import re
# 1 关键字 2 分界符 3 运算符 4 关系运算符 5 常数 6 标识符 0 Error
keys = ("char", "double", "enum", "float", "int", "long", "short",
        "signed", "struct", "union", "unsigned", "void", "for",
        "do", "while", "break", "continue", "if", "else", "goto",
        "switch", "case", "default", "return", "auto", "extern",
        "register", "static", "const", "sizeof", "typedef", "volatile")
delimiters = (";", ",", "(", ")", "[", "]")
operators = ("=", "+", "+=", "-", "-=", "*", "*=",
             "/", "/=", "&", "&&", "|", "||", "!", ".", "->")
relations = ("!=", "==", "<", ">", "<=", ">=")
consts = []
ids = []

type_table = {1: keys, 2: delimiters,
              3: operators, 4: relations, 5: consts, 6: ids}

R = {}

output = open("clean_code.c", "w", encoding="utf-8")


def check(state, morphere):
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


def FSM(word, col):
    morphere = []
    start = 0  # 标记词素的起始位置
    end = 0  # 标记词素的结束
    state = 0  # 标记词素类型 0为空
    for char in word:
        end += 1
        state = R[state](char)
        if state == 2 or state == 4:
            morphere.append(check(state, word[start:end]))
            start = end  # 遍历下一个词素
            state = 0


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
