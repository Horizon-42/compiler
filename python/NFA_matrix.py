#规定X为起始状态 Y为终结状态 N表示不可到达 e表示空
def init(infile):
    input = open(infile, 'r')
    s_str = input.readline()
    S = s_str.split()
    e_str = input.readline()
    E = e_str.split()
    input.close()
    return [S,E]

def get_R(infile,S,E):
    R = {}
    for s in S:
        for e in E:
            if s in R:
                R[s].update({e:[]})
            else: 
                R.update({s:{e:[]}}) 

    input = open(infile, "r")
    while True:
        r_str=input.readline()
        if not r_str:
            break
        r=r_str.split()
        R[r[0]][r[1]].append(r[2])
    input.close()

    for s in S:
        for e in E:
            print(R[s][e],end=' ')
        print()
    return R

def is_in(Ie,ia):
    for ie in Ie:
        if ie==ia:
            return True
    return False

def no_repeat(I):
    res=[]
    for i in I:
        if i not in res:
            res.append(i)
    return res

def e_close_i(J,R):
    I=J
    bnr=len(J)
    i=0
    while i<bnr:
        if(not R[I[i]]['e']==[]):
            I=I+R[I[i]]['e']
            I = no_repeat(I)
            bnr=len(I)
        i=i+1
    I.sort()
    if(len(I)):
        return ''.join(I)
    else: 
        return '$'

def e_close_j(I,a,R):
    Ia=[]
    for i in I:
        if(R[i][a]!=[]):
            Ia=Ia+R[i][a]  
            Ia = no_repeat(Ia)  
    Ia.sort()     
    return Ia


def get_I(S,E,R):
    Ie=[e_close_i(['X'],R)]
    I={Ie[0]:{'e':Ie[0]}}
    for ie in Ie:
        for a in E[1:]:
            j = e_close_j(list(ie),a,R)
            ia = e_close_i(j,R)
            I[ie].update({a:ia})
            if(not is_in(Ie,ia) and ia!='$'):
                Ie.append(ia)
                I.update({ia:{'e':ia}})
    
    
    for ie in Ie:
        for a in E:
            print(I[ie][a]+'\t\t',end=' ')
        print()

    return [Ie,I]

def get_DFA_I(Ie,E,I):
    DFA_I={}
    I_S={}
    for i in range(0,len(Ie)):
        I_S.update({Ie[i]:i})

    for i in range(0,len(Ie)):
        for a in E:
            if I[ Ie[i] ][a] == '$':
                DFA_I[i].update({a:'$'})
            else:
                if i in DFA_I:
                    DFA_I[i].update({a:I_S[ I[ Ie[i] ][a] ]})
                else: 
                    DFA_I.update({i:{a:I_S[ I[ Ie[i] ][a] ]}})

            
    
    for i in range(0,len(Ie)):
        for a in E:
            print(DFA_I[i][a],end=' ')
        print()
    
    return DFA_I


if __name__ == '__main__':
    [S,E]=init('NFA.in')
    print(S)
    R=get_R('NFA_R.in',S,E)
    print()
    [Ie,I]=get_I(S,E,R)
    print()
    get_DFA_I(Ie,E,I)