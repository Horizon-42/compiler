from stack import Stack

# 终结符 ε符号代表空
Vt = ()
# 非终结符 规定第一个非终结符必须是文法开始符号
Vn = ()
M = {}


def initV():
    global Vt, Vn
    try:
        input = open('V.i', 'r', encoding='utf-8').read()
        vs = input.split(';')
        assert len(vs) == 2, '在V.in中输入终结符与非终结符，用";"隔开'
        Vn = tuple(vs[0].split())
        Vt = tuple(vs[1].split())
    except IOError as Error:
        print(Error)
    except AssertionError as AError:
        print(AError)


def initM():
    global Vn, Vt, M
    productions = {}
    # 读取产生式
    try:
        input = open('Grammar.i', 'r', encoding='utf-8')
        for line in input:
            pro = line.split('->')
            assert len(pro) == 2, '产生式输入格式为 "E->e1|e2"'
            # 分割候选式

            def split(candidates):
                candidates = candidates.strip('\n')
                syms = candidates.split('|')
                syms = filter(lambda x: x, syms)
                return list(syms)
            # 更新产生式字典
            if pro[0] not in M:
                productions.update({pro[0]: split(pro[1])})
            else:
                productions[pro[0]] += split(pro[1])
    except IOError as Error:
        print(Error)
    except AssertionError as AError:
        print(AError)
    # print(productions)
    # 获取FIRST
    FIRST = {}

    def get_first(X):
        # 终结符
        def add_to_first(X, a):
            if X in FIRST:
                FIRST[X].add(a)
            else:
                FIRST.update({X: {a}})
        if X == 'ε':
            add_to_first(X, 'ε')
        elif X in Vt:
            add_to_first(X, X)
            return
        # 非终结符
        else:
            for candidate in productions[X]:
                get_first(candidate[0])
                # X->a...
                if candidate[0] in Vt or candidate[0] == 'ε':
                    add_to_first(X, candidate[0])
                else:
                    # X->Y...
                    for a in FIRST[candidate[0]]:
                        if a != 'ε':
                            add_to_first(X, a)
                    # X->Y1Y2Y3...
                    peek = 0
                    for sym in candidate:
                        peek += 1
                        get_first(sym)
                        if sym in Vn and 'ε' in FIRST[sym]:
                            if peek == len(candidate):
                                add_to_first(X, 'ε')
                            else:
                                get_first(candidate[peek])
                                for a in FIRST[candidate[peek]]:
                                    if a != 'ε':
                                        add_to_first(X, a)
                        else:
                            break
    for v in Vt:
        get_first(v)
    for v in Vn:
        get_first(v)
    # print('FIRST:')
    # for v in Vn:
    #     print("%s: %s" % (v, FIRST[v]))
    # 获取FOLLOW
    FOLLOW = {}
    # 如果FOLLOW有更新，返回TRUE 否则返回FALSE

    def get_follow(X):
        assert X in Vn, "get_follow(%s), 非法参数，只对非终结符求FOLLOW集合" % X
        has_change = False

        def add_to_follow(X, a):
            nonlocal has_change
            if X not in FOLLOW:
                FOLLOW.update({X: {a}})
                has_change = True
            elif a not in FOLLOW[X]:
                FOLLOW[X].add(a)
                has_change = True
        if X == Vn[0]:
            add_to_follow(X, '#')
        for candidate in productions[X]:
            peek = 0
            for B in candidate:
                peek += 1
                # X->αB
                if B in Vt or B == 'ε':
                    continue
                elif peek == len(candidate):
                    if X in FOLLOW:
                        for a in FOLLOW[X]:
                            add_to_follow(B, a)
                # X->αBβ
                else:
                    empty = False
                    for a in FIRST[candidate[peek]]:
                        if a != 'ε':
                            add_to_follow(B, a)
                        else:
                            empty = True
                    # X->αBβ and ε in FIREST(β)
                    if empty and X in FOLLOW:
                        for a in FOLLOW[X]:
                            add_to_follow(B, a)
        return has_change

    try:
        changed = True
        while changed:
            changed = False
            for v in Vn:
                changed = changed | get_follow(v)
    except AssertionError as AError:
        print(AError)
    # print('FOLLW:')
    # for v in Vn:
    #     print("%s: %s" % (v, FOLLOW[v]))

    # 构造M
    Vt_end = list(Vt)
    Vt_end.append('#')
    # print(Vt)
    for A in Vn:
        for a in Vt_end:
            if A in M:
                M[A].update({a: False})
            else:
                M.update({A: {a: False}})
    # print(M)
    for A in Vn:
        for cand in productions[A]:
            empty = False
            for a in FIRST[cand[0]]:
                M[A][a] = cand
                if a == 'ε':
                    empty = True
            if empty:
                for b in FOLLOW[A]:
                    M[A][b] = cand

    # for A in Vn:
    #     for a in Vt_end:
    #         print("%s -> %3s" % (A, M[A][a]), end='\t')
    #     print()


def analysis(sym_str):
    sym_str += '#'
    syms = Stack()
    syms.push('#')
    syms.push(Vn[0])
    step = 0
    pro = ''
    action = 'INIT'
    i = 0
    a = sym_str[i]
    print("步骤              符号栈            输入串            所用产生式        动作              ")
    print("%-18s%-18s%-18s%-18s%-18s" %
          (step, syms, sym_str[i::], pro, action))
    while i < len(sym_str):
        step += 1
        pro = ''
        X = syms.pop()
        action = 'POP'
        if X in Vt:
            if X == a:
                i += 1
                a = sym_str[i]
                action = "Get Next"
            else:
                raise ValueError(
                    'Syntactic Error: %s is not expected here' % a)
        elif X == '#':
            if X == a:
                return True
            else:
                raise ValueError(
                    'Syntactic Error: %s is not expected here' % a)
        elif M[X][a]:
            vs = M[X][a]
            pro = "%s->%s" % (X, vs)
            if vs != 'ε':
                action += ", PUSH(%s)" % vs[::-1]
                for v in vs[::-1]:
                    syms.push(v)
        else:
            raise ValueError('Syntactic Error: %s is not expected here' % a)
        print("%-18s%-18s%-18s%-18s%-18s" %
              (step, syms, sym_str[i::], pro, action))

    return False


if __name__ == '__main__':
    initV()
    initM()
    try:
        analysis('i+i*i')
    except ValueError as Error:
        print(Error)
