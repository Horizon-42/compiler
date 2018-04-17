S=[]
E=[]

def init(infile):
    input = open(infile, 'r')
    s_str = input.readline()
    S = s_str.split()
    e_str = input.readline()
    E = e_str.split()
    input.close()
    return [S,E]

def get_mat(infile, S, E):
    R = {}
    for s in S:
        for e in E:
            if s in R:
                R[s].update({e:S[0]})
            else: 
                R.update({s:{e:S[0]}})

    input = open(infile, "r")
    while True:
        r_str=input.readline()
        if not r_str:
            break
        r=r_str.split()
        R[r[0]][r[1]]=r[2]
    input.close()
    return R

if __name__ == '__main__':
    [S,E]=init('DFA.in')
    for s in S:
        print(s, end='')
    print()
    for e in E:
        print(e, end='')
    print()
    R = get_mat("DFA_R.in", S, E)
    for s in S:
        for e in E:
            print(R[s][e], end=' ')
        print()
    