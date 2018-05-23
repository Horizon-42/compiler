import re


def read(infile, outfile):
    input = open(infile, "r", encoding="utf-8")
    output = open(outfile, "w", encoding="utf-8")
    code = []
    annotation = False
    for line in input:
        # 移除回车
        line = line.strip('\n')  # strip 移除字符串头尾指定到字符
        line = line.strip(' ')  # 移除多余空格及制表符
        if not annotation:
            # 删除多行注释
            if len(line) >= 2 and line[0] == '/'and line[1] == '*':
                annotation = True
                continue
            # 删除单行注释
            pattern = r"//.*"
            line = re.sub(pattern, '', line)
            # 删除空行
            if line == ' ' or line == '':
                continue
            code.append(line)
            print(line)
            output.write(line+"\n")
        else:
            if len(line) >= 2 and line[-1] == '/'and line[-2] == '*':
                annotation = False
    return code


if __name__ == "__main__":
    code = read("test.c", "clean_code.c")
    print()
    print()
    print(code)
